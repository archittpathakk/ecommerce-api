from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Review(Base):
    """
    Represents a user-submitted review for a product.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="review_rating_check"
        ),
        UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_user_product_review"
        ),
    )
