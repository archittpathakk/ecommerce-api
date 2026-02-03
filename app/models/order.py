# app/models/order.py

import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    order_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    status = Column(
        Enum(
            OrderStatus,
            name="orderstatus",
            create_type=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=OrderStatus.PENDING.value
    )

    user = relationship("User", back_populates="orders")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
