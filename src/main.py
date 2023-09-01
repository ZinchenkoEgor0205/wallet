from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.pages.router import router as router_pages, fastapi_users
from src.common_deposit.router import router as router_common_deposit
from src.crypto_deposit.router import router as router_crypto_deposit
from src.router import router as router_main

app = FastAPI(
    title='Wallet'
)



app.mount('/src/static', StaticFiles(directory='src/static'), name='static')

app.include_router(router_main)
app.include_router(router_pages)
app.include_router(router_common_deposit)
app.include_router(router_crypto_deposit)




app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)