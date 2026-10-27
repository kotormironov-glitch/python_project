import pytest
from sqlalchemy.orm import Session
from classes.api_manager import ApiManager
from db.models.credit_table import Credit
from src.main.api.models.credit_request import CreditRequest, CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

@pytest.mark.api
class TestCredit:
    def test_credit_request(self, db_session: Session, before_bank_operation, api_manager: ApiManager):
        user_request, account = before_bank_operation
        response = api_manager.user_steps.to_credite(
            user_request,
            CreditRequest(accountId=user_request.id, amount=500, termMonths=12)
        )

        assert response.balance == account.amount + 500
        assert response.termMonths == 12
        assert response.amount == 500
        assert response.balance == response.amount
        assert response.creditId == 5
        assert response.accountId == account.id

        credit_from_db = Credit.get_credit_by_account_id(db_session, user_request.id)
        assert credit_from_db.amount == response.amount, "Нет созданной записи кредита"

    def test_credit_repay(self, db_session: Session, before_bank_operation, api_manager: ApiManager):
        user_request, account = before_bank_operation
        сredit = api_manager.user_steps.to_credite(
            user_request,
            CreditRequest(accountId=user_request.id, amount=500, termMonths=12)
        )
        response = api_manager.user_steps.to_repay(user_request, CreditRepayRequest(creditId=сredit.id, amount=500, accountId=сredit.accountId))

        assert response.amountDeposited == 500

        credit_from_db = Credit.get_credit_by_account_id(db_session, user_request.id)
        assert credit_from_db.amount == 0, "Кредит не погашен"

    def test_max_invalid_credit_request(self, db_session: Session, before_bank_operation, api_manager: ApiManager):
        amount = 15001
        user_request, account = before_bank_operation

        response = api_manager.user_steps.to_credite(
            user_request,
            CreditRequest(accountId=user_request.id, amount=amount, termMonths=12)
        )

        assert response.balance == account.amount + 500
        assert response.termMonths == 12
        assert response.amount == amount
        assert response.balance == response.amount
        assert response.creditId == 5
        assert response.accountId == account.id

        credit_from_db = Credit.get_credit_by_account_id(db_session, user_request.id)
        assert credit_from_db.amount == response.amount, "Нет созданной записи кредита"

    def test_invalid_repay(self, db_session: Session, before_bank_operation, api_manager: ApiManager):
        amount = 2
        user_request, account = before_bank_operation

        сredit = api_manager.user_steps.to_credite(
            user_request,
            CreditRequest(accountId=user_request.id, amount=500, termMonths=12)
        )
        response = api_manager.user_steps.to_repay(user_request, CreditRepayRequest(creditId=сredit.id, amount=amount, accountId=сredit.accountId))

        assert response.amountDeposited == amount

        credit_from_db = Credit.get_credit_by_account_id(db_session, user_request.id)
        assert credit_from_db.amount == 0, "Кредит не погашен"