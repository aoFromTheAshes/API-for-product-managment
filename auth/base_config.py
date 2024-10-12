from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, exceptions, models, schemas

from .models import User
from .manager import get_user_manager

from dotenv import load_dotenv
import os

load_dotenv()

cookie_transport = CookieTransport(
    cookie_name="bonds",  # Назва кукі
    cookie_max_age=3600,  # Час життя кукі в секундах (1 година)
    cookie_path="/",      # Шлях дії кукі
    cookie_secure=True,   # Встановіть True для використання лише через HTTPS
    cookie_httponly=True, # HTTP only для захисту від XSS атак
)

SECRET = os.getenv('SECRET')

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,  # Функція для отримання менеджера користувачів
    [auth_backend],    # Список бекендів для аутентифікації
)

current_user = fastapi_users.current_user()