import csv
import io 
from sqlalchemy.orm import Session
from fastapi import UploadFile
from backend.app.etl.core import process_and_validate_rows

async def process_transaction_csv_ETL(db: Session, file: UploadFile):
    contents = await file.read()
    reader = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    bad_rows = []

    rows = list(reader)
    valid_rows, bad_rows = process_and_validate_rows(db=db, rows=rows)
    actual_rows = len(valid_rows)

    return bad_rows, actual_rows


    
