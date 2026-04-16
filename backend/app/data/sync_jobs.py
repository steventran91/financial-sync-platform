from datetime import datetime

from backend.app.models.sync_job import SyncJob


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