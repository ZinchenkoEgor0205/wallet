from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Float)
from sqlalchemy.orm import DeclarativeBase

from src.auth.models import User


class Base(DeclarativeBase):
    pass


class CryptoDeposit(Base):
    __tablename__ = "CryptoDeposit"

    id = Column(Integer, primary_key=True)
    type: str = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    api_key: str = Column(String, nullable=False)
