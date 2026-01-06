from pydantic import BaseModel
from typing import Optional

class PaymentSessionCreate(BaseModel):
    amount: int  # Amount in cents
    success_url: str
    cancel_url: str

class PaymentSessionOut(BaseModel):
    session_id: str
    checkout_url: str
