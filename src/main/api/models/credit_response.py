from src.main.api.models.base_model import BaseModel

class CreditResponse(BaseModel):
    account_id: int
    amount: int
    term_months: int
    balance: int
    credit_id: int

class CreditRepayResponse(BaseModel):
    credit_id: int
    amount_deposited: int