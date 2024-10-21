from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import crud, schemas, models
from ..database import get_async_session

router = APIRouter(
    prefix="/category",
    tags=["categories"]
)

@router.get("/", response_model=list[schemas.Category])
async def categories(db: AsyncSession = Depends(get_async_session)):
    category_list = await crud.get_categories(db=db)
    return category_list

@router.post("/create", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_async_session)):
    db_item = models.Category(name=category.name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.patch("/update/{category_id}", response_model=schemas.Category)
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
