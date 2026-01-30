from pydantic import BaseModel
from decimal import Decimal

from .category import CategoryOut

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int

class ProductCreate(ProductBase):
    category_id: int

class ProductUpdate(ProductCreate):
    pass

class ProductOut(ProductBase):
    id: int

    category: CategoryOut

    class Config:
        from_attributes = True