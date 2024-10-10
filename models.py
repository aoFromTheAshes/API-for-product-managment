from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

from auth.models import Base

# Модель категорій
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Відношення з таблицею продуктів
    products = relationship("Product", back_populates="category")


# Модель продуктів
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)  # Використовуємо Text для великих описів
    price = Column(Float, nullable=False)  # Float або Numeric для цін з копійками
    category_id = Column(Integer, ForeignKey('categories.id'))  # ForeignKey до таблиці 'categories'
    stock_quantity = Column(Integer)  # Кількість на складі
    created_at = Column(TIMESTAMP, server_default=func.now())  # Автоматична дата створення
    updated_at = Column(TIMESTAMP, onupdate=func.now(), server_default=func.now())  # Автоматична дата оновлення

    # Відношення з таблицею категорій
    category = relationship("Category", back_populates="products")
