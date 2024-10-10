from fastapi import FastAPI
from .auth.base_config import fastapi_users, auth_backend
from .auth.schemas import UserRead, UserCreate, UserUpdate  # Не забудьте імпортувати UserUpdate

app = FastAPI()

# Маршрути для автентифікації
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth/jwt", 
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),  # Додайте UserUpdate
    prefix="/users",
    tags=["users"]
)

