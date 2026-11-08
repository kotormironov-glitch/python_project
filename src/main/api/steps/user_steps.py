from typing import Any, Optional, Literal

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def to_send_request(
            self,
            create_user_request: CreateUserRequest,
            endpoint: Endpoint,
            response_specs: RequestSpecs,
            body: Optional[Any] = None):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint,
            response_specs
        ).post(body)
        return response

    def create_account(self, create_user_request: CreateUserRequest):
        return self.to_send_request(
            create_user_request,
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        )

    def to_deposit(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_DEPOSIT,
            ResponseSpecs.request_ok(),
            body
        )

    def to_deposit_invalid(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_DEPOSIT,
            ResponseSpecs.request_bad(),
            body
        )

    def to_transfer(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_TRANSFER,
            ResponseSpecs.request_ok(),
            body
        )

    def to_transfer_invalid(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_TRANSFER,
            ResponseSpecs.request_bad(),
            body
        )

    def to_credit(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_CREDIT,
            ResponseSpecs.request_created(),
            body
        )

    def to_credit_invalid(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_CREDIT,
            ResponseSpecs.request_bad(),
            body
        )

    def to_repay(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_REPAY,
            ResponseSpecs.request_ok(),
            body
        )

    def to_repay_invalid(self, create_user_request: CreateUserRequest, body: Any):
        return self.to_send_request(
            create_user_request,
            Endpoint.TO_REPAY,
            ResponseSpecs.request_unprocessable_content(),
            body
        )