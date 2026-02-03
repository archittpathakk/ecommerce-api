# app/routers/cart.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from app import models, schemas, dependencies

router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"]
)

# ---------------------------------------------------
# GET /cart/  → View cart
# ---------------------------------------------------
@router.get("/", response_model=schemas.CartOut)
def get_user_cart(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    cart = current_user.cart

    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    total_price = sum(
    Decimal(str(item.product.price)) * item.quantity
    for item in cart.items
    )


    return schemas.CartOut(
    items=[schemas.CartItemOut.model_validate(item) for item in cart.items],
    total_price=total_price,
    )



# ---------------------------------------------------
# POST /cart/items  → Add item to cart
# ---------------------------------------------------
@router.post(
    "/items",
    response_model=schemas.CartItemOut,
    status_code=status.HTTP_201_CREATED
)
def add_item_to_cart(
    item_data: schemas.CartItemAdd,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    cart = current_user.cart
    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = (
        db.query(models.Product)
        .filter(models.Product.id == item_data.product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == product.id
        )
        .first()
    )

    if cart_item:
        new_quantity = cart_item.quantity + item_data.quantity
        if new_quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )
        cart_item.quantity = new_quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item

    if item_data.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    cart_item = models.CartItem(
        cart_id=cart.id,
        product_id=product.id,
        quantity=item_data.quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return schemas.CartItemOut.model_validate(cart_item)



# ---------------------------------------------------
# PUT /cart/items/{product_id}  → Update quantity
# ---------------------------------------------------
@router.put(
    "/items/{product_id}",
    response_model=schemas.CartItemOut
)
def update_cart_item_quantity(
    product_id: int,
    item_data: schemas.CartItemUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    cart = current_user.cart
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == product_id
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if item_data.quantity > cart_item.product.stock:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)

    return schemas.CartItemOut.model_validate(cart_item)



# ---------------------------------------------------
# DELETE /cart/items/{product_id}  → Remove item
# ---------------------------------------------------
@router.delete(
    "/items/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    cart = current_user.cart
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == product_id
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    db.delete(cart_item)
    db.commit()
    return None


# ---------------------------------------------------
# DELETE /cart/  → Clear cart
# ---------------------------------------------------
@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def clear_cart(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    cart = current_user.cart
    if cart and cart.items:
        cart.items.clear()
        db.commit()
    return None
