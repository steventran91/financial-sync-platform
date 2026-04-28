from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class SyncJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    provider_id: int
    job_type: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    records_processed: int
    records_failed: int