# app/schemas/cart.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from decimal import Decimal
# Import ProductOut schema to nest product details within the cart item response.
from .product import ProductOut

# --- Cart Item Schema ---
# This schema will represent a single item within a user's cart.
class CartItemOut(BaseModel):
    product: ProductOut
    quantity: int

    model_config = ConfigDict(from_attributes=True)




# --- Cart Schema ---
# This schema represents the entire shopping cart.
class CartOut(BaseModel):
    items: List[CartItemOut]
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)





class CartItemAdd(BaseModel):
    """
    Schema for the data required to add a new item to the cart.
    """
    product_id: int
    # We use Pydantic's Field to add validation. The quantity must be
    # an integer that is "greater than" 0. This prevents users from
    # adding zero or a negative number of items to their cart.
    quantity: int = Field(gt=0, description="The quantity of the product to add.")


class CartItemUpdate(BaseModel):
    """
    Schema for updating the quantity of an item already in the cart.
    """
    # Just like when adding, the quantity must be a positive integer.
    # We enforce this with Pydantic's Field validation.
    quantity: int = Field(gt=0, description="The new quantity for the cart item.")