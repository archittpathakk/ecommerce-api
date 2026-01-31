# app/schemas/cart.py

from pydantic import BaseModel
from typing import List

# Import ProductOut schema to nest product details within the cart item response.
from .product import ProductOut

# --- Cart Item Schema ---
# This schema will represent a single item within a user's cart.
class CartItemOut(BaseModel):
    """
    Schema for an item returned from the cart. It includes the quantity
    and the full product details.
    """
    quantity: int

    # This is the key part for nesting. The 'product' field will be populated
    # with data that conforms to the ProductOut schema. Pydantic will automatically
    # handle the serialization of the nested SQLAlchemy 'product' relationship object.
    product: ProductOut

    class Config:
        # Enable ORM mode to allow creating this Pydantic model from a
        # SQLAlchemy ORM object.
        from_attributes = True

# --- Cart Schema ---
# This schema represents the entire shopping cart.
class CartOut(BaseModel):
    """
    Schema for the entire shopping cart, including its ID and a list of all items.
    """
    id: int

    # The 'items' field will be a list, where each element in the list
    # conforms to the CartItemOut schema we defined above.
    items: List[CartItemOut]

    class Config:
        from_attributes = True