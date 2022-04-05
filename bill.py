from pydantic import BaseModel


class Bill(BaseModel):
    billReceiver: int
    billPayer: int
    payDate: str 
    payedValue: float