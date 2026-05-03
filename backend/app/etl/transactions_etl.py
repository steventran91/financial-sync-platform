import csv
import io 
from sqlalchemy.orm import Session
from fastapi import UploadFile
from pydantic import ValidationError
from backend.app.models.create_transaction import CreateTransactionRequest
from backend.app.services.transaction_service import create_transaction

async def process_transaction_csv_ETL(db: Session, file: UploadFile):
    contents = await file.read()
    reader = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    bad_rows = []

    for row in reader:
        try:
            transaction = CreateTransactionRequest(
                amount = row["amount"],
                transaction_date = row["transaction_date"],
                merchant = row["merchant"],
                sync_job_id = row["sync_job_id"],
            )
            create_transaction(db=db, payload=transaction)

        except ValidationError as e:
            bad_rows.append({"row": dict(row), "error": str(e)})

    return bad_rows


    
