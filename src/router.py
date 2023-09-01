

from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import UserRead
from src.common_deposit.models import CommonDeposit
from src.common_deposit.schemas import CommonDepositRead
from src.crypto_deposit.models import CryptoDeposit
from src.crypto_deposit.schemas import OKXCredentials
from src.crypto_deposit.utills import get_okx_balance
from src.database import get_async_session
from src.pages.router import fastapi_users, templates
from sqlalchemy import select, Column, insert

router = APIRouter(
    prefix="/main",
    tags=["Main"]
)

current_user = fastapi_users.current_user()


@router.get('/')
async def get_main(request: Request, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    username = user.username
    query = await db.execute(
        select(User, CommonDeposit, CryptoDeposit).join(CommonDeposit, User.id == CommonDeposit.user_id).join(
            CryptoDeposit, User.id == CryptoDeposit.user_id).where(User.username == username))
    deposits = {'common': {}, 'crypto': {}}
    okx_api_key = ''
    for row in query:
        deposits['common'][row[1].id] = {'deposit_sum': row[1].sum, 'deposit_income': row[1].income}
        deposits['crypto'][row[2].id] = {'type': row[2].type, 'api_key': row[2].api_key}
        if row[2].type == 'OKX':
            okx_api_key = row[2].api_key

    okx_phrase = request.cookies.get('okx_phrase')
    okx_key = request.cookies.get('okx_key')
    if okx_phrase and okx_key and okx_api_key:
        okx_balance = get_okx_balance(okx_api_key, okx_key, okx_phrase)
        print(okx_balance)


    return {'user': username, 'deposits': deposits}


@router.post('/')
async def post_main(okx_credentials: OKXCredentials, response: Response):
    if okx_credentials.phrase and okx_credentials.secret_key:
        response.set_cookie(key='okx_phrase', value=okx_credentials.phrase)
        response.set_cookie(key='okx_key', value=okx_credentials.secret_key)
    return {'message': 'cookies are well done'}
