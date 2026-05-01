from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from pydantic import field_validator

class CreateTransactionRequest(BaseModel):
    amount: Decimal
    transaction_date: datetime
    merchant: str
    sync_job_id: int 


    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value


    @field_validator("transaction_date")
    @classmethod
    def validate_transaction_date(cls, transaction_date):
        if transaction_date > datetime.now(tz=transaction_date.tzinfo):
            raise ValueError("Invalid transaction date. Transaction date is in the future")
        return transaction_date
    
