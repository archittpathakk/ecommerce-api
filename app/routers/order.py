from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app import models, schemas, dependencies

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# ---------------------------------------------------
# POST /orders/ → Create order from cart (USER)
# ---------------------------------------------------
@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    cart = current_user.cart

    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an order from an empty cart.",
        )

    try:
        
        for cart_item in cart.items:
            if cart_item.quantity > cart_item.product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient stock",
                )

        
        order = models.Order(user_id=current_user.id)
        db.add(order)
        db.flush()

        order_items: list[models.OrderItem] = []

        for cart_item in cart.items:
            product = cart_item.product

            order_item = models.OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                price=product.price,
            )

            db.add(order_item)
            order_items.append(order_item)

            product.stock -= cart_item.quantity

        
        cart.items.clear()

        
        db.commit()

        total_price = sum(
            item.price * item.quantity for item in order_items
        )

        return schemas.OrderOut(
            id=order.id,
            status=order.status,
            total_price=Decimal(total_price),
            items=[
                schemas.OrderItemOut(
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.price,
                )
                for item in order_items
            ],
        )

    except HTTPException:
        db.rollback()
        raise


# ---------------------------------------------------
# GET /orders/ → Get current user's orders
# ---------------------------------------------------
@router.get("/", response_model=List[schemas.OrderOut])
def get_user_orders(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .order_by(models.Order.order_date.desc())
        .all()
    )

    result: list[schemas.OrderOut] = []

    for order in orders:
        total_price = sum(
            item.price * item.quantity for item in order.items
        )

        result.append(
            schemas.OrderOut(
                id=order.id,
                status=order.status,
                total_price=Decimal(total_price),
                items=[
                    schemas.OrderItemOut(
                        product=item.product,
                        quantity=item.quantity,
                        price_at_purchase=item.price,
                    )
                    for item in order.items
                ],
            )
        )

    return result

# ---------------------------------------------------
# GET /orders/{order_id} → Order details (USER)
# ---------------------------------------------------
@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_user_order_details(
    order_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found.",
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order.",
        )

    total_price = sum(
        item.price * item.quantity for item in order.items
    )

    return schemas.OrderOut(
        id=order.id,
        status=order.status,
        total_price=Decimal(total_price),
        items=[
            schemas.OrderItemOut(
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.price,
            )
            for item in order.items
        ],
    )
