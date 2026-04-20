from typing import Literal 
from pydantic import BaseModel

class CreateSyncJobRequest(BaseModel):
    provider_id: int
    job_type: Literal["payments", "refunds", "adjustments"]
    status: Literal["pending", "running", "completed", "failed"]


