from fastapi import Depends, HTTPException, status
import models
from .base_config import current_active_user  # Використовуємо відносний шлях для імпорту
from sqlalchemy import select
from .models import User
from ..database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user_with_role(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    # Виконуємо запит до бази для отримання ролі користувача через role_id
    result = await db.execute(select(models.Role).where(models.Role.id == user.role_id))
    user_role = result.scalars().first()

    if user_role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not found.")
    
    return user, user_role

# Функція для перевірки, чи користувач має потрібну роль
async def check_user_role(required_role: str, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    # Отримуємо користувача і його роль через попередню функцію
    user, user_role = await get_current_user_with_role(user, db)

    # Перевіряємо, чи відповідає роль користувача вимогам
    if user_role.name != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource.")
    
    return user  # Якщо все ок, повертаємо користувача
