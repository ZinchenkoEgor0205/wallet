from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.common_deposit.models import CommonDeposit
from src.crypto_deposit.models import CryptoDeposit
from src.crypto_deposit.schemas import BrockerCredentials
from src.crypto_deposit.utills import get_binance_data, get_okx_data, get_crypto_sum
from src.database import get_async_session
from src.pages.router import fastapi_users
from sqlalchemy import select

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
    okx_api_key, binance_api_key = '', ''
    for row in query:
        deposits['common'][row[1].id] = {'deposit_sum': row[1].sum, 'deposit_income': row[1].income}
        okx_api_key = row[2].okx_api_key
        binance_api_key = row[2].binance_api_key

    await get_okx_data(okx_api_key, deposits, request)

    await get_binance_data(binance_api_key, deposits, request)
    deposits['crypto']['total_cost_USDT'] = get_crypto_sum(deposits['crypto'])
    return {'user': username, 'deposits': deposits}


# noinspection DuplicatedCode
@router.post('/cookie-OKX')
async def post_cookie_okx(okx_credentials: BrockerCredentials, response: Response, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    if okx_credentials.phrase and okx_credentials.secret_key:
        response.set_cookie(key='okx_phrase', value=okx_credentials.phrase)
        response.set_cookie(key='okx_key', value=okx_credentials.secret_key)
    query = await db.execute(select(User, CryptoDeposit).join(CryptoDeposit, User.id == CryptoDeposit.user_id).where(User.username == user.username))
    for row in query:
        row[1].okx_api_key = okx_credentials.api_key
    await db.commit()
    return {'message': 'cookies are well done'}


# noinspection DuplicatedCode
@router.post('/cookie-Binance')
async def post_cookie_binance(binance_credentials: BrockerCredentials, response: Response,
                              user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    if binance_credentials.phrase and binance_credentials.secret_key:
        response.set_cookie(key='binance_phrase', value=binance_credentials.phrase)
        response.set_cookie(key='binance_key', value=binance_credentials.secret_key)

    query = await db.execute(select(User, CryptoDeposit).join(CryptoDeposit, User.id == CryptoDeposit.user_id).where(User.username == user.username))
    for row in query:
        row[1].binance_api_key = binance_credentials.api_key
    await db.commit()
    return {'message': 'cookies are well done'}
