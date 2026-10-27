import pytest
from sqlalchemy.orm import Session
from classes.api_manager import ApiManager
from generators.model_generator import RandomModelGenerator
from src.main.api.models.account_request import DepositRequest, TransferRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction

@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.admin_steps.create_user(create_user_request)
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        response = api_manager.user_steps.to_deposit(create_user_request, DepositRequest(accountId=create_account_response.id, amount=1000.5))

        assert response.balance == 1000.5
        assert response.id == create_account_response.id

        deposit_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert deposit_from_db.balance == response.balance, 'Депозин не был внесен'

    def test_transfer_account(self, db_session: Session, before_test_transfer_account, api_manager: ApiManager):
        response1, response2, role_1, role_2 = before_test_transfer_account

        transfer_request = TransferRequest(fromAccountId=response1.id, toAccountId=response2.id, amount=500.75)

        result = api_manager.user_steps.to_transfer(role_1, transfer_request)

        assert result.fromAccountId == response1.id
        assert result.toAccountId == response2.id
        assert result.fromAccountIdBalance == 499.75

        transfer_from_db = Transaction.get_transaction_from_account_id(db_session, response1.id)
        assert transfer_from_db.from_account_id == response1.id, "Запись с переводом не создалась"

    def test_invalid_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        amount = 999

        api_manager.admin_steps.create_user(create_user_request)
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        response = api_manager.user_steps.to_deposit(create_user_request, DepositRequest(accountId=create_account_response.id, amount=amount))

        assert response.balance == amount
        assert response.id == create_account_response.id

        deposit_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert deposit_from_db.balance == response.balance, 'Депозин не был внесен'

    def test_invalid_transfer_account(self, db_session: Session, before_test_transfer_account, api_manager: ApiManager):
        amount = 0
        response1, response2, role1, role2 = before_test_transfer_account

        transfer_response = TransferRequest(fromAccountId=response1.id, toAccountId=response2.id, amount=amount)

        result = api_manager.user_steps.to_transfer_invalid(role1, transfer_response)

        assert result.text == '{"error":"Amount must be greater than 0\\nAmount must be between 500 and 10000"}'