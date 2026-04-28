from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal



class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    transaction_date: datetime
    created_at: datetime
    amount: Decimal
    merchant: str
    status: str
    sync_job_id: int