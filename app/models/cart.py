from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="cart")
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("carts.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
