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
def get_sync_jobs():
    return sync_jobs


@app.get("/sync-jobs/{job_id}")
def get_sync_job(job_id: int):
    for job in sync_jobs:
        if job.id == job_id:
            return job


    raise HTTPException(status_code=404, detail="Sync job not found")