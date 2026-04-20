from typing import Optional

from backend.app.data.sync_jobs import sync_jobs
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

