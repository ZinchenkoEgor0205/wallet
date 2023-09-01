
from pydantic import BaseModel


class CommonDepositRead(BaseModel):
    id: int
    sum: float
    income: float
    user_id: int

    class Config:
        orm_mode = True

