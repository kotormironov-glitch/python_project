import pytest

from src.main.api.models.credit_request import CreditRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_request import DepositRequest, TransferRequest
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.fixture
def create_user(api_manager):
    def _create(role: str = "ROLE_USER"):
        user = RandomModelGenerator.generate(CreateUserRequest, role=role)
        api_manager.admin_steps.create_user(user)
        account = api_manager.user_steps.create_account(user)
        return user, account
    return _create

@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def before_test_transfer_account(api_manager: ApiManager):
    role_1 = RandomModelGenerator.generate(CreateUserRequest)
    role_2 = RandomModelGenerator.generate(CreateUserRequest)

    api_manager.admin_steps.create_user(role_1)
    api_manager.admin_steps.create_user(role_2)

    account_1 = api_manager.user_steps.create_account(role_1)
    account_2 = api_manager.user_steps.create_account(role_2)

    deposit_request_1 = RandomModelGenerator.generate(
        DepositRequest, accountId=account_1.id
    )
    deposit_request_2 = RandomModelGenerator.generate(
        DepositRequest, accountId=account_2.id
    )

    deposit1 = api_manager.user_steps.to_deposit(role_1, deposit_request_1)
    deposit2 = api_manager.user_steps.to_deposit(role_2, deposit_request_2)

    # сумма перевода должна влезать в депозит
    transfer_amount = min(deposit_request_1.amount, deposit_request_2.amount) / 2
    transfer_model = TransferRequest(
        fromAccountId=account_1.id,
        toAccountId=account_2.id,
        amount=transfer_amount
    )

    return deposit1, deposit2, role_1, role_2, transfer_model, deposit_request_1.amount-transfer_amount


@pytest.fixture
def before_bank_operation(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    account = api_manager.user_steps.create_account(user_request)
    return user_request, account

@pytest.fixture
def user(before_bank_operation):
    user, _ = before_bank_operation
    return user

@pytest.fixture
def account(before_bank_operation):
    _, account = before_bank_operation
    return account

@pytest.fixture
def deposit_request(account):
    model_obj = RandomModelGenerator.generate(DepositRequest, accountId=account.id)
    return DepositRequest(accountId=account.id, amount=model_obj.amount)

@pytest.fixture
def amount(deposit_request: DepositRequest) -> float:
    return deposit_request.amount

@pytest.fixture()
def before_test_deposit_account(api_manager: ApiManager, before_bank_operation):
    user_request, account = before_bank_operation

    model_obj = RandomModelGenerator.generate(DepositRequest)

    return user_request, DepositRequest(accountId=account.id, amount=model_obj.amount), model_obj.amount, account

@pytest.fixture

def create_user_for_credit(api_manager: ApiManager, create_user):
    user, account = create_user("ROLE_CREDIT_SECRET")
    return user, account

@pytest.fixture
def create_credit(api_manager: ApiManager, create_user_for_credit):
    user, account = create_user_for_credit
    credit_request = RandomModelGenerator.generate(CreditRequest, accountId=account.id)
    return user, account, api_manager.user_steps.to_credit(user, credit_request)