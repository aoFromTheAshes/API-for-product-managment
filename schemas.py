from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int

# Схема для створення нового продукту
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    stock_quantity: Optional[int] = None

class ProductUpdate(ProductBase):
    description: str
    stock_quantity: Optional[int] = None
    

class Product(ProductBase):
    id: int
    description: str
    stock_quantity: int
    created_at: datetime = Field(..., description="Date of product creation")
    updated_at: datetime = Field(..., description="Product update date")
    
    class Config:
        orm_mode = True
        
class Category(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        
class CategoryCreate(BaseModel):
    name: str