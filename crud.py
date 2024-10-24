from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Імпорт з поточної папки
from . import models as main_models, schemas as main_schemas

# Імпорт з папки auth
from .auth import models as auth_models, schemas as auth_schemas


# Отримати продукт за id
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(main_models.Product).filter(main_models.Product.id == product_id))
    return result.scalar_one_or_none()


# Отримати продукт за назвою
async def get_product_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(main_models.Product).filter(main_models.Product.name == name))
    return result.scalar_one_or_none()


# Отримати всі продукти з підтримкою пропуску (skip) та ліміту (limit)
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(main_models.Product).offset(skip).limit(limit))
    return result.scalars().all()


# Створити новий продукт
async def create_product(db: AsyncSession, product: main_schemas.ProductCreate):
    db_item = main_models.Product(
        name=product.name, 
        description=product.description, 
        price=product.price, 
        category_id=product.category_id, 
        stock_quantity=product.stock_quantity
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


# Отримати опис продукту
async def get_product_description(db: AsyncSession, product_id: int):
    result = await db.execute(select(main_models.Product.description).filter(main_models.Product.id == product_id))
    product_description = result.scalars().first()
    return product_description if product_description else None


# Оновити всю інформацію про продукт
async def change_full_product(db: AsyncSession, product_id: int, product: main_schemas.ProductUpdate):
    result = await db.execute(select(main_models.Product).filter(main_models.Product.id == product_id))
    result = result.scalars().first()

    if result:
        result.name = product.name
        result.description = product.description
        result.price = product.price
        result.category_id = product.category_id
        result.stock_quantity = product.stock_quantity

        await db.commit()
        await db.refresh(result)
    
    return result


# Отримати всі категорії
async def get_categories(db: AsyncSession):
    result = await db.execute(select(main_models.Category))
    return result.scalars().all()
