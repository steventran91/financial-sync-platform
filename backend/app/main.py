from typing import Optional, List
from fastapi import FastAPI, HTTPException
from backend.app.models.sync_job import SyncJob
from backend.app.services.sync_job_service import list_sync_jobs, get_sync_job_by_id

app = FastAPI(title="Financial Sync Platform API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Financial Sync Platform API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sync-jobs", response_model=List[SyncJob])
def get_sync_jobs(status: Optional[str] = None):
    return list_sync_jobs(status=status)


@app.get("/sync-jobs/{job_id}", response_model=SyncJob)
def get_sync_job(job_id: int):
    job = get_sync_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Sync job not found")

    return job