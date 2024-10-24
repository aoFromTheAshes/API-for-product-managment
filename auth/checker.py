from fastapi import Depends, HTTPException, status
from .models import User, Role  # Використовуємо відносний шлях для імпорту
from .base_config import current_active_user  # Використовуємо відносний шлях для імпорту
from sqlalchemy import select
from ..database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user_with_role(required_roles: list[str], user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    # Виконуємо запит до бази для отримання ролі користувача через role_id
    result = await db.execute(select(Role).where(Role.id == user.role_id))
    user_role = result.scalars().first()

    if user_role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not found.")

    # Перевіряємо, чи роль користувача відповідає необхідній ролі
    if user_role.name not in required_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
    
    return user


