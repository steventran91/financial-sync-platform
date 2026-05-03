from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.models.transaction import TransactionDB
from backend.app.models.transaction import Transaction
from backend.app.models.update_transaction import UpdateTransactionRequest
from backend.app.models.create_transaction import CreateTransactionRequest




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


def list_transactions(
        db: Session, 
        merchant: Optional[str] = None, 
        sync_job_id: Optional[int] = None, 
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Transaction]:
    
    transaction = select(TransactionDB)

    if status is not None:
        transaction = transaction.where(TransactionDB.status == status)
    if merchant is not None:
        transaction = transaction.where(TransactionDB.merchant == merchant)
    if sync_job_id is not None:
        transaction = transaction.where(TransactionDB.sync_job_id == sync_job_id)

    transaction = transaction.limit(limit).offset(offset)

    rows = db.scalars(transaction).all()
    return [Transaction.model_validate(row) for row in rows]

def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    row = db.get(TransactionDB, transaction_id)
    if row is None:
        return None
    return Transaction.model_validate(row)


def update_transaction(db: Session, transaction_id: int, payload: UpdateTransactionRequest) -> Optional[Transaction]:
    row = db.get(TransactionDB, transaction_id)

    if row is None:
        return None
    
    row.status = payload.status
    
    db.commit()
    db.refresh(row)
    return Transaction.model_validate(row)


def delete_transaction(db: Session, transaction_id: int) -> bool:
    transaction = db.get(TransactionDB, transaction_id)

    if transaction is None:
        return False

    db.delete(transaction)
    db.commit()
    return True 

