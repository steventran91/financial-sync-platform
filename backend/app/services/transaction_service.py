from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.models.transaction import TransactionDB
from backend.app.models.transaction import Transaction
from backend.app.models.create_transaction import CreateTransactionRequest


def list_transactions(db: Session) -> List[Transaction]:
    transaction = select(TransactionDB)

    rows = db.scalars(transaction).all()
    return [Transaction.model_validate(row) for row in rows]

def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    row = db.get(TransactionDB, transaction_id)
    if row is None:
        return None
    return Transaction.model_validate(row)

def create_transaction(db: Session, payload: CreateTransactionRequest) -> Transaction:
    row = TransactionDB(
        amount = payload.amount,
        transaction_date = payload.transaction_date,
        merchant = payload.merchant,
        sync_job_id = payload.sync_job_id,
        created_at = datetime.now(),
        status = "pending"
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return Transaction.model_validate(row)

