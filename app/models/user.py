# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="customer")

    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
