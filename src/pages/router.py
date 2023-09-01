from typing import List, Dict

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import manager
from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

templates = Jinja2Templates(directory="src/templates")

current_user = fastapi_users.current_user()

@router.get("/main")
def get_base_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def post_login(request: Request, data: OAuth2PasswordRequestForm = Depends(),  db: AsyncSession = Depends(get_async_session)) -> \
dict[str, str]:
    username = data.username

    password = data.password
    print(username)
    print(1)
    # user_query = await db.get(User, ident=1)
    results = await db.execute(select(User).where(User.username == username))
    # user = results.scalar()
    # if password != user.hashed_password:
    #     raise InvalidCredentialsException
    # user = results.scalars().where(username=username)
    # print(user.username)
    # print(users)
    # user = User.from_orm(user_query)

    # user = await load_user(username)
    # print(user)
    # print(password)
    # print(user_query.username)
    # access_token = manager.create_access_token(
    #     data=dict(sub=username)
    # )

    # return {'access_token': access_token, 'token_type': 'bearer'}
    return {'test': '1'}
    # return templates.TemplateResponse("login.html", {"request": request, 'access_token': access_token, 'token_type': 'bearer'})