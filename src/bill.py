from pydantic import BaseModel
from typing import Optional


class Bill(BaseModel):
    billReceiver: int
    billPayer: int
    payDate: str 
    payedValue: float

class UpdateBill(BaseModel):
    billReceiver: Optional[int]
    billPayer: Optional[int]
    payDate: Optional[str] 
    payedValue: Optional[float]