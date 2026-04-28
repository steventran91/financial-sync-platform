from datetime import datetime 
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.db.models.sync_job import SyncJobDB
from backend.app.models.create_sync_job import CreateSyncJobRequest
from backend.app.models.sync_job import SyncJob

def list_sync_jobs(db: Session, status: Optional[str] = None) -> list[SyncJob]:
    stmt = select(SyncJobDB)

    if status is not None:
        stmt = stmt.where(SyncJobDB.status == status)

    rows = db.scalars(stmt).all()
    return [SyncJob.model_validate(row) for row in rows]


def get_sync_job_by_id(db: Session, job_id: int) -> Optional[SyncJob]:
    row = db.get(SyncJobDB, job_id)
    if row is None:
        return None
    return SyncJob.model_validate(row)


def create_sync_job(db: Session, payload: CreateSyncJobRequest) -> SyncJob:
    row = SyncJobDB(
        provider_id = payload.provider_id,
        job_type=payload.job_type,
        status=payload.status,
        started_at=datetime.now(),
        completed_at=None,
        records_processed=0,
        records_failed=0,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return SyncJob.model_validate(row)
