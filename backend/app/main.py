from fastapi import FastAPI, HTTPException
from datetime import datetime
from backend.app.models.sync_job import SyncJob

app = FastAPI(title="Financial Sync Platform API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Financial Sync Platform API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

# Fake in-memory data (we will replace with DB later)
sync_jobs = [
    SyncJob(
        id=1,
        provider_id=1001,
        job_type="payments",
        status="completed",
        started_at=datetime.now(),
        completed_at=datetime.now(),
        records_processed=100,
        records_failed=2,
    ),
    SyncJob(
        id=2,
        provider_id=1002,
        job_type="refunds",
        status="running",
        started_at=datetime.now(),
        completed_at=None,
        records_processed=50,
        records_failed=0,
    ),
]


@app.get("/sync-jobs")
def get_sync_jobs():
    return sync_jobs

@app.get("/sync-jobs/{job_id}")
def get_sync_job(job_id: int):
    for job in sync_jobs:
        if job.id == job_id:
            return job


    raise HTTPException(status_code=404, detail="Sync job not found")