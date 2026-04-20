from datetime import datetime 
from typing import Optional, List

from backend.app.data.sync_jobs import sync_jobs
from backend.app.models.create_sync_job import CreateSyncJobRequest
from backend.app.models.sync_job import SyncJob

def list_sync_jobs(status: Optional[str] = None) -> list[SyncJob]:
    if status is None:
        return sync_jobs

    return [job for job in sync_jobs if job.status == status]


def get_sync_job_by_id(job_id: int) -> Optional[SyncJob]:
    for job in sync_jobs:
        if job.id == job_id:
            return job

    return None


def create_sync_job(payload: CreateSyncJobRequest) -> SyncJob:
    next_id = len(sync_jobs) + 1

    new_job = SyncJob(
        id=next_id,
        provider_id=payload.provider_id,
        job_type=payload.job_type,
        status=payload.status,
        started_at=datetime.now(),
        completed_at=None,
        records_processed=0,
        records_failed=0,
    )

    sync_jobs.append(new_job)
    return new_job
