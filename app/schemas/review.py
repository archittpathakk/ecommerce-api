# app/schemas/review.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from .user import UserOut


class ReviewCreate(BaseModel):
    
    product_id: int

    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating from 1 to 5",
    )

    comment: Optional[str] = Field(
        None,
        max_length=1000,
    )


class ReviewOut(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
