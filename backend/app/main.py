from typing import Optional, List
from sqlalchemy import text
from backend.app.db.session import engine 
from fastapi import FastAPI, HTTPException
from backend.app.models.sync_job import SyncJob
from backend.app.models.create_sync_job import CreateSyncJobRequest
from backend.app.services.sync_job_service import list_sync_jobs, get_sync_job_by_id, create_sync_job

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

@app.get("/sync-jobs", response_model=List[SyncJob])
def get_sync_jobs(status: Optional[str] = None):
    return list_sync_jobs(status=status)


@app.get("/sync-jobs/{job_id}", response_model=SyncJob)
def get_sync_job(job_id: int):
    job = get_sync_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Sync job not found")

    return job

@app.post("/sync-jobs", response_model=SyncJob)
def create_new_sync_job(payload: CreateSyncJobRequest):
    return create_sync_job(payload)