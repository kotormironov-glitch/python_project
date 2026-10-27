import requests

from src.main.api.models.account_request import DepositRequest, TransferRequest
from src.main.api.models.account_response import DepositResponse, TransferResponse
from src.main.api.requests.requester import Requester


class DepositAccountRequester(Requester):
    def post(self, deposit_request: DepositRequest) -> DepositResponse:
        url=f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=deposit_request.model_dump(),
        )
        self.response_spec(response)
        return DepositResponse(**response.json())

class TransferAccountRequester(Requester):
    def post(self, transfer_request: TransferRequest) -> TransferResponse:
        url=f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=transfer_request.model_dump(),
        )
        self.response_spec(response)
        return TransferResponse(**response.json())