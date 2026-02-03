from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import List, Optional

from .category import CategoryOut
from .review import ReviewOut


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
    )
    price: Decimal = Field(
        ...,
        gt=Decimal("0.00"),
        decimal_places=2,
    )
    stock: int = Field(
        ...,
        ge=0,
    )
    category_id: int

    model_config = ConfigDict(
    json_schema_extra={
        "examples": [
            {
                "name": "Pro Wireless Mouse",
                "description": "An ergonomic, high-performance wireless mouse for professionals.",
                "price": "79.99",
                "stock": 150,
                "category_id": 1,
            }
        ]
    }
)



class ProductCreate(ProductBase):
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=Decimal("0.00"), decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class ProductOut(ProductBase):
    id: int
    category: CategoryOut
    reviews: List[ReviewOut] = []
    average_rating: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
