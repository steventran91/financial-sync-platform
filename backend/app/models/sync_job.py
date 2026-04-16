from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SyncJob(BaseModel):
    id: int
    provider_id: int
    job_type: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    records_processed: int
    records_failed: int