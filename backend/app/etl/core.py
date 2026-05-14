from pydantic import ValidationError
from backend.app.models.create_transaction import CreateTransactionRequest
from backend.app.services.transaction_service import create_transaction
from sqlalchemy.orm import Session

def process_and_validate_rows(db: Session, rows: dict) -> tuple:
    valid_rows = []
    bad_rows = []
    for row in rows:
        try:
            transaction = CreateTransactionRequest(
                amount = row["amount"],
                transaction_date = row["transaction_date"],
                merchant = row["merchant"],
                sync_job_id = row["sync_job_id"],
            )
            valid_transaction = create_transaction(db=db, payload=transaction)
            valid_rows.append(valid_transaction)
        except ValidationError as e:
            bad_rows.append({"row": dict(row), "error": str(e)})

    return valid_rows, bad_rows

def load_valid_rows_to_db(db: Session, valid_rows: dict) -> None:
    for row in valid_rows:
        payload = CreateTransactionRequest(**row)
        create_transaction(db=db, payload=payload)