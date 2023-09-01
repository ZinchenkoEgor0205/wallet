from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Float)
from sqlalchemy.orm import DeclarativeBase

from src.auth.models import User


class Base(DeclarativeBase):
    pass


class CommonDeposit(Base):
    __tablename__ = "CommonDeposit"

    id = Column(Integer, primary_key=True)
    sum: float = Column(Float, nullable=False)
    income: float = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
