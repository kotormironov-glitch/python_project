from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from models.account_request import DepositRequest, TransferRequest
from models.account_response import DepositResponse, TransferResponse
from models.create_account_response import CreateAccountResponse
from models.credit_request import CreditRequest, CreditRepayRequest
from models.credit_response import CreditResponse, CreditRepayResponse
from models.login_user_request import LoginUserRequest
from models.login_user_response import LoginUserResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model=CreateAccountResponse
    )

    TO_DEPOSIT = EndpointConfiguration(
        request_model=DepositRequest,
        url="/account/deposit",
        response_model=DepositResponse
    )

    TO_TRANSFER = EndpointConfiguration(
        request_model=TransferRequest,
        url="/account/transfer",
        response_model=TransferResponse
    )

    TO_CREDIT = EndpointConfiguration(
        request_model=CreditRequest,
        url="/credit/request",
        response_model=CreditResponse
    )

    TO_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse
    )
