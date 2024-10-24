from fastapi import FastAPI, Depends
from .auth.base_config import fastapi_users, auth_backend
from .auth.schemas import UserRead, UserCreate, UserUpdate  


from fastapi import FastAPI
from .auth.base_config import fastapi_users, auth_backend, current_active_user
from .routers import products, categories  # Імпортуємо окремі роутери

from .auth.checker import get_current_user_with_role
from .auth.models import User, Role
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_async_session

app = FastAPI()

# Підключаємо автентифікаційні маршрути
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

# Підключаємо інші маршрути
app.include_router(products.router)
app.include_router(categories.router)


@app.get("/restricted-route")
async def restricted_route(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["admin", "manager"], user=user, db=db)
    return {"message": f"Hello {user.email}, you have access to this route."}
