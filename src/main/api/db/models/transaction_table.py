from sqlalchemy import Column, Integer, ForeignKey, String, Float, TIMESTAMP, VARCHAR
from db.base import Base


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    to_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    from_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'<Transaction(id={self.id}, to_account_id={self.to_account_id}), from_account_id={self.from_account_id}), credit_id={self.credit_id}, amount={self.amount}, transaction_type={self.transaction_type}, created_at={self.created_at}>'