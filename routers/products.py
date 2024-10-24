from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select

from .. import crud, schemas, models
from ..database import get_async_session

from ..auth.base_config import current_active_user
from ..auth.checker import get_current_user_with_role
from ..auth.models import User

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=list[schemas.Product])
async def get_all_products(skip: int = 0, limit: int = 100, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["user", "manager", "admin"], user=user, db=db)
    
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}/description", response_model=str)
async def get_description_by_id(product_id: int, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["user", "manager", "admin"], user=user, db=db)
    
    description = await crud.get_product_description(db, product_id)
    
    if description is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return description

@router.post("/create", response_model=schemas.Product)
async def add_new_product(product: schemas.ProductCreate, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["user", "manager", "admin"], user=user, db=db)

    
    return await crud.create_product(product=product, db=db)

@router.put("/{product_id}/update", response_model=schemas.Product)
async def change_products(product_id: int, product: schemas.ProductUpdate, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["manager", "admin"], user=user, db=db)    
    
    db_product = await crud.change_full_product(db, product_id, product=product)
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return db_product

@router.delete("/{product_id}/delete")
async def delete_product(product_id: int, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    user = await get_current_user_with_role(["admin"], user=user, db=db)
    
    product = await crud.get_product(db, product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await db.delete(product)
    await db.commit() 

    return {"detail": "Product deleted successfully"}

@router.get("/search")
async def search_products(
    id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    category_id: Optional[int] = None,
    stock_quantity: Optional[int] = None,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user_with_role(["user", "manager", "admin"], user=user, db=db)
    
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
