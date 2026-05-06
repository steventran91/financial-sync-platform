from typing import Optional, List
from sqlalchemy import text
from backend.app.db.session import engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from backend.app.models.sync_job import SyncJob
from backend.app.models.create_sync_job import CreateSyncJobRequest
from backend.app.models.create_transaction import CreateTransactionRequest
from backend.app.services.sync_job_service import list_sync_jobs, get_sync_job_by_id, create_sync_job
from backend.app.services.transaction_service import list_transactions, get_transaction_by_id, create_transaction, update_transaction, delete_transaction
from backend.app.models.transaction import Transaction
from backend.app.models.update_transaction import UpdateTransactionRequest
from backend.app.etl.transactions_etl import process_transaction_csv_ETL
from fastapi import UploadFile, File


app = FastAPI(title="Financial Sync Platform API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Financial Sync Platform API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/db-health")
def db_health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {"database": "ok", "result": value}

@app.post("/sync-jobs", response_model=SyncJob)
def create_new_sync_job(payload: CreateSyncJobRequest, db: Session = Depends(get_db)):
    return create_sync_job(db=db, payload=payload)


@app.get("/sync-jobs", response_model=List[SyncJob])
def get_sync_jobs(db: Session = Depends(get_db), status: Optional[str] = None):
    return list_sync_jobs(db=db, status=status)


@app.get("/sync-jobs/{job_id}", response_model=SyncJob)
def get_sync_job(job_id: int, db: Session = Depends(get_db)):
    job = get_sync_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Sync job not found")

    return job


@app.post("/transactions", response_model=Transaction)
def create_new_transaction(payload: CreateTransactionRequest, db: Session = Depends(get_db)):
    return create_transaction(db=db, payload=payload)


@app.get("/transactions", response_model=List[Transaction])
def get_transactions(limit: int= 20, offset: int = 0, status: Optional[str] = None, merchant: Optional[str] = None, sync_job_id: Optional[int] = None, db: Session = Depends(get_db)):
    return list_transactions(db=db, limit=limit, offset=offset, status=status, merchant=merchant, sync_job_id=sync_job_id)

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@app.patch("/transactions/{transaction_id}", response_model=Transaction)
def patch_transaction(payload: UpdateTransactionRequest, transaction_id: int, db: Session = Depends(get_db)):
    updated_transaction = update_transaction(db=db, payload=payload, transaction_id=transaction_id)

    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction ID does not exist")
    
    return updated_transaction

@app.delete("/transactions/{transaction_id}")
def delete_txn(transaction_id: int, db: Session = Depends(get_db)):
    deleted_txn = delete_transaction(db=db, transaction_id=transaction_id)

    if deleted_txn:
        return {"message": "Transaction deleted"}
    else:
        raise HTTPException(status_code=404, detail="Transaction ID not found")
    

@app.post("/transactions/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    errors,  actual_rows = await process_transaction_csv_ETL(db=db, file=file)
    return {"message": "upload complete.", "rows_processed": actual_rows, "errors": errors}
        

