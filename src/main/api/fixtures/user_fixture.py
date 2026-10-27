import pytest

from classes.api_manager import ApiManager
from generators.model_generator import RandomModelGenerator
from models.account_request import DepositRequest
from models.create_user_request import CreateUserRequest

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

    response = api_manager.user_steps.to_deposit(
        role_1, DepositRequest(accountId=account_1.id, amount=1000.5)
    )
    response2 = api_manager.user_steps.to_deposit(
        role_2, DepositRequest(accountId=account_2.id, amount=1000.5)
    )

    return response, response2, role_1, role_2


@pytest.fixture
def before_bank_operation(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    account = api_manager.user_steps.create_account(user_request)
    return user_request, account