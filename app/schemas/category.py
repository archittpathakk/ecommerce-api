# app/schemas/category.py

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """
    Base schema for a product category, containing the category's name.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.
    """
    pass # No additional fields are needed for creation.


class CategoryOut(CategoryBase):
   
    id: int


    model_config = ConfigDict(from_attributes=True)
