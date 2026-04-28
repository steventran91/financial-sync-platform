from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class CreateTransactionRequest(BaseModel):
    amount: Decimal
    transaction_date: datetime
    merchant: str
    sync_job_id: int 