# app/schemas/order.py

from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
from decimal import Decimal

# We need the ProductOut schema to nest product details within the order item response.
from .product import ProductOut
from .user import UserOut
from ..models import OrderStatus


# --- Order Item Schema ---
# This schema defines the structure for a single item within a created order.
class OrderItemOut(BaseModel):
    product: ProductOut
    quantity: int
    price_at_purchase: Decimal

    model_config = ConfigDict(from_attributes=True)

# --- Order Schema ---
# This schema represents the entire order.
class OrderOut(BaseModel):
    id: int
    total_price: Decimal
    status: OrderStatus
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)



class AdminOrderOut(OrderOut):
    user: UserOut

    model_config = ConfigDict(from_attributes=True)



class OrderStatusUpdate(BaseModel):
    
    status: OrderStatus