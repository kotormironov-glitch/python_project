from typing import Annotated
from generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class DepositRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(refex=r'^[1000-9000]$')]

class TransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[float, CreationRule(refex=r'^[500-10000]$')]