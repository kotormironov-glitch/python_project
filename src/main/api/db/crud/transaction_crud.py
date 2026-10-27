from sqlalchemy.orm import Session
from db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_to_account_id(db: Session, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=to_account_id).first()

    @staticmethod
    def get_transaction_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).first()