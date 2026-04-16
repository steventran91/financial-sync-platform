from typing import Optional
from fastapi import FastAPI, HTTPException
from backend.app.data.sync_jobs import sync_jobs

app = FastAPI(title="Financial Sync Platform API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Financial Sync Platform API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sync-jobs")
def get_sync_jobs(status: Optional[str] = None):
    if status is None:
        return sync_jobs
    
    filtered_jobs = [job for job in sync_jobs if job.status == status]
    return filtered_jobs


@app.get("/sync-jobs/{job_id}")
def get_sync_job(job_id: int):
    for job in sync_jobs:
        if job.id == job_id:
            return job


    raise HTTPException(status_code=404, detail="Sync job not found")