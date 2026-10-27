import requests

from src.main.api.models.credit_request import CreditRequest, CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse, CreditRepayResponse
from src.main.api.requests.requester import Requester


class CreditRequester(Requester):
    def post(self, deposit_request: CreditRequest) -> CreditResponse:
        url=f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=deposit_request.model_dump(),
        )
        self.response_spec(response)
        return CreditResponse(**response.json())

class CreditRepayRequester(Requester):
    def post(self, transfer_request: CreditRepayRequest) -> CreditRepayResponse:
        url=f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=transfer_request.model_dump(),
        )
        self.response_spec(response)
        return CreditRepayResponse(**response.json())