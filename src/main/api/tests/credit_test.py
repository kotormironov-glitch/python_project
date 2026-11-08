import pytest
from sqlalchemy.orm import Session

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.credit_table import Credit
from src.main.api.models.credit_request import CreditRequest, CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

@pytest.mark.api
class TestCredit:
    def test_credit_request(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit
    ):
        user, account, credit = create_credit
        assert credit.termMonths in range(1, 13)
        assert credit.balance == credit.amount
        assert credit.id == account.id

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.amount == credit.amount, "Нет созданной записи кредита"

    def test_credit_repay(self, db_session: Session, api_manager: ApiManager, create_credit):
        user, account, credit = create_credit
        response = api_manager.user_steps.to_repay(user, CreditRepayRequest(creditId=credit.creditId, amount=credit.amount, accountId=account.id))

        assert response.amountDeposited == credit.amount

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.balance == 0, "Кредит не погашен"

    @pytest.mark.parametrize("amount", [1, 4999, 15001])
    def test_max_invalid_credit_request(self, db_session: Session, api_manager: ApiManager, create_user_for_credit, amount):
        user, account = create_user_for_credit

        response = api_manager.user_steps.to_credit_invalid(
            user,
            RandomModelGenerator.generate(CreditRequest, accountId=account.id, amount=amount)
        )

        assert response.text == '{"error":"Amount must be between 5000 and 15000"}'

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db == None, "Есть созданная запись кредита"

    @pytest.mark.parametrize("amount", [1, 4999])
    def test_invalid_repay(self, db_session: Session, api_manager: ApiManager, create_credit, amount):
        user, account, credit = create_credit

        response = api_manager.user_steps.to_repay_invalid(user, CreditRepayRequest(creditId=credit.creditId, amount=amount, accountId=account.id))

        assert '{"error":"The amount is not enough. Credit balance: ' in response.text

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.amount != 0, "Кредит погашен"