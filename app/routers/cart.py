# app/routers/cart.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies

# Create a new router instance for cart-related endpoints.
router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"]
)

@router.get("/", response_model=schemas.CartOut)
def get_user_cart(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Retrieve the current authenticated user's shopping cart.

    If the user does not have a cart, one will be created for them automatically.
    This endpoint is protected and requires a valid JWT token.
    """
    # The `get_current_user` dependency gives us the authenticated user object.
    # Thanks to the `user.cart` relationship we defined in the models,
    # SQLAlchemy can lazily load the cart associated with this user.
    cart = current_user.cart

    # Handle the case where a user (especially a new one) doesn't have a cart yet.
    if not cart:
        # Create a new Cart instance and associate it with the current user.
        new_cart = models.Cart(user_id=current_user.id)
        db.add(new_cart)
        db.commit()
        # Refresh the user object to load the newly created cart relationship.
        db.refresh(current_user)
        # Re-assign the cart variable to the newly created cart.
        cart = current_user.cart

    # Return the user's cart. FastAPI will use the CartOut schema to serialize
    # this object, including the list of items and their nested product details.
    # If the cart is new and empty, it will correctly return an empty 'items' list.
    return cart