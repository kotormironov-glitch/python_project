from typing import Annotated
from generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class CreditRequest(BaseModel):
    accountId: int
    amount: Annotated[int, CreationRule(refex=r'^[5000-15000]$')]
    termMonths: Annotated[int, CreationRule(refex=r'^[1-12]$')]

class CreditRepayRequest(BaseModel):
    credit_id: int
    account_id: int
    amount: int