from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.models.transaction import TransactionDB
from backend.app.models.transaction import Transaction


def list_transactions(db: Session) -> List[Transaction]:
    transaction = select(TransactionDB)

    rows = db.scalars(transaction).all()
    return [Transaction.model_validate(row) for row in rows]

def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    row = db.get(TransactionDB, transaction_id)
    if row is None:
        return None
    return Transaction.model_validate(row)

