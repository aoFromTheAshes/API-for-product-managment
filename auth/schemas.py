from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    pass

class UserCreate(schemas.BaseUserCreate):
    username: str  # Додайте це поле

class UserUpdate(schemas.BaseUserUpdate):
    pass
