from urllib.request import Request

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.common_deposit.models import CommonDeposit
from src.database import get_async_session
from src.pages.router import fastapi_users, templates
from sqlalchemy import select, Column, insert

router = APIRouter(
    prefix="/common_deposit",
    tags=["CommonDeposit"]
)


current_user = fastapi_users.current_user()


@router.get("/")
async def get_common_deposits(user: User = Depends(current_user),  db: AsyncSession = Depends(get_async_session)):
    query = await db.execute(select(User, CommonDeposit).join(CommonDeposit, User.id == CommonDeposit.user_id).where(User.username == user.username))
    print(query.first()[0].username)
    return {'test': 1}


@router.post('/')
async def post_common_deposit(sum: float, income: float, user: User = Depends(current_user),  db: AsyncSession = Depends(get_async_session)):
    await db.execute(insert(CommonDeposit).values(sum=sum, income=income, user_id=user.id))
    await db.commit()
    return {'test': 2}
