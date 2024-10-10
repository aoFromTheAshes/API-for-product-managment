from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel

class RoleRead(BaseModel):
    id: int
    name: str
    permissions: Optional[dict] = None

    class Config:
        orm_mode = True

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role: Optional[RoleRead]  # Зв'язок з роллю

    class Config:
        orm_mode = True
        
class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: Optional[int]  # Тут передається id ролі
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    
class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None  # id ролі для оновлення
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False