from urllib.request import Request

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.crypto_deposit.models import CryptoDeposit
from src.database import get_async_session
from src.pages.router import fastapi_users, templates
from sqlalchemy import select, Column, insert

router = APIRouter(
    prefix="/crypto_deposit",
    tags=["CryptoDeposit"]
)

current_user = fastapi_users.current_user()


@router.get("/")
async def get_crypto_deposits(user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    username = user.username
    query = await db.execute(
        select(User, CryptoDeposit).join(CryptoDeposit, User.id == CryptoDeposit.user_id).where(User.username == username))
    deposits = {}
    for row in query:
        deposits[row[1].id] = {'type': row[1].type, 'api_key': row[1].api_key}
    return {'user': username, 'deposits': deposits}


@router.post('/')
async def post_crypto_deposits(type: str, api_key: str, user: User = Depends(current_user),
                    db: AsyncSession = Depends(get_async_session)):
    await db.execute(insert(CryptoDeposit).values(type=type, api_key=api_key, user_id=user.id))
    await db.commit()
    return {'test': 2}
