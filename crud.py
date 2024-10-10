from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


# Отримати користувача за id
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).filter(models.Product.id == product_id))
    return result.scalar_one_or_none()


# Отримати користувача за email
async def get_product_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Product).filter(models.Product.name == name))
    return result.scalar_one_or_none()


# Отримати всіх користувачів з підтримкою пропуску (skip) та ліміту (limit)
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()


# Створити нового користувача
async def create_product(db: AsyncSession, product: schemas.Product):
    db_item = models.Product(name=product.name, description=product.description, price=product.price, category_id=product.category_id, stock_quantity=product.stock_quantity)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

