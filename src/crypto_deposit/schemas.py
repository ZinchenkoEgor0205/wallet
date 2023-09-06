from typing import Optional

from pydantic import BaseModel


class CryptoDepositRead(BaseModel):
    id: int
    type: str
    api_key: str
    user_id: int

    class Config:
        orm_mode = True


class BrockerCredentials(BaseModel):
    api_key: Optional[str] = ''
    secret_key: Optional[str] = ''
    phrase: Optional[str] = ''
