# app/routers/admin_order.py

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import models, schemas, dependencies


router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin - Orders"],
    dependencies=[Depends(dependencies.get_current_admin_user)]
)


@router.get("/", response_model=List[schemas.AdminOrderOut])
def get_all_orders(
    db: Session = Depends(dependencies.get_db),
    skip: int = Query(default=0, ge=0, description="The number of items to skip"),
    limit: int = Query(default=100, ge=1, le=250, description="The maximum number of items to return")
):
    """
    Retrieve a list of all orders from all users. Admin access is required.
    Includes pagination to handle large numbers of orders.
    """
    orders = (
        db.query(models.Order)
        .options(joinedload(models.Order.user))
        .order_by(models.Order.order_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return orders


@router.patch("/{order_id}", response_model=schemas.AdminOrderOut)
def update_order_status(
    order_id: int,
    order_update: schemas.OrderStatusUpdate,
    db: Session = Depends(dependencies.get_db)
):
    """
    Update the status of a specific order. Admin access is required.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found."
        )

    order.status = order_update.status

    db.commit()
    db.refresh(order)

    return order
