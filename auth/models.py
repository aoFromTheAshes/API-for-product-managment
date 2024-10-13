from datetime import timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class Base(DeclarativeBase):
    pass
jhh
# Модель ролей
class Role(Base):
    __tablename__ = "role"  # Ви назвали цю таблицю "role", а не "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


a = 1
# Модель користувачів
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"  # Рекомендується використовувати множину

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())  # Оновлено для коректності
    role_id = Column(Integer, ForeignKey("role.id"))  # Тут правильна назва таблиці "role"
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

