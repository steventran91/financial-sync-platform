from typing import Literal
from pydantic import BaseModel

class UpdateTransactionRequest(BaseModel):
    status: Literal["pending", "completed", "failed"]