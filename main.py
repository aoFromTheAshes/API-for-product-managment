from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from .auth.base_config import fastapi_users, auth_backend
from .auth.schemas import UserRead, UserCreate, UserUpdate  # Не забудьте імпортувати UserUpdate
from .auth.models import User
from .auth.base_config import current_user

from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_async_session
from sqlalchemy import select

from . import crud, schemas, models

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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/products/", response_model=list[schemas.Product])
async def get_all_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    products = await crud.get_products(db, skip=skip, limit=limit)  
    return products

    
@app.get("/products/{product_id}/description", response_model=str)
async def get_description_by_id(product_id: int, db: AsyncSession = Depends(get_async_session)):
    description = await crud.get_product_description(db, product_id)
    
    if description is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return description
    
    
@app.post("/products/create", response_model=schemas.Product)
async def add_new_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud.create_product(product=product, db=db)


@app.put("/products/{product_id}/update", response_model=schemas.Product)
async def change_products(product_id: int, product: schemas.ProductUpdate,db: AsyncSession = Depends(get_async_session)):
    db_product = await crud.change_full_product(db, product_id, product=product)
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return db_product


@app.delete("/products/{product_id}/delete")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    product = await crud.get_product(db, product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await db.delete(product)
    await db.commit() 

    return {"detail": "Product deleted successfully"}


@app.get("/products/search")
async def search_products(
    id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    category_id: Optional[int] = None,
    stock_quantity: Optional[int] = None,
    db: AsyncSession = Depends(get_async_session)
):
    query = select(models.Product)

    if id is not None:
        query = query.filter(models.Product.id == id)
    if name is not None:
        query = query.filter(models.Product.name == name)
    if description is not None:
        query = query.filter(models.Product.description == description)
    if price is not None:
        query = query.filter(models.Product.price == price)
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if stock_quantity is not None:
        query = query.filter(models.Product.stock_quantity == stock_quantity)

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    return products


@app.get("/category/", response_model=list[schemas.Category])
async def categories(db: AsyncSession = Depends(get_async_session)):
    category_list = await crud.get_categories(db=db)
    return category_list


@app.post("/category/create", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_async_session)):
    db_item = models.Category(name=category.name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@app.patch("/category/update/{category_id}", response_model=schemas.Category)
async def get_updated(category_id: int, new_category: schemas.CategoryUpdate, db: AsyncSession = Depends(get_async_session)):
    category = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    category = category.scalars().first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if new_category.name is not None:
        category.name = new_category.name

    await db.commit()
    await db.refresh(category)
    
    return category
