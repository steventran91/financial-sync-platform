from typing import Literal 
from pydantic import BaseModel

class CreateSyncJobRequest(BaseModel):
    provider_id: int
    job_type: str
    status: Literal["pending", "running", "completed", "failed"]


