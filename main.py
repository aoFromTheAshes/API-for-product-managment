from fastapi import FastAPI, Depends, HTTPException
from .auth.base_config import fastapi_users, auth_backend
from .auth.schemas import UserRead, UserCreate, UserUpdate  # Не забудьте імпортувати UserUpdate
from .auth.models import User
from .auth.base_config import current_user

from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_async_session

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
async def delete_product(product_id: int,db: AsyncSession = Depends(get_async_session)):
    product = await crud.get_product(db, product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
