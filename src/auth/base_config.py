
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from src.config import SECRET_AUTH

cookie_transport = CookieTransport(cookie_name="wallet", cookie_max_age=36000, cookie_samesite='none', cookie_httponly=False, cookie_domain='127.0.0.1')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=36000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

