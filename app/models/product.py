from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category")

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    # -------------------------------------------------
    # Hybrid property: average_rating
    # -------------------------------------------------

    @hybrid_property
    def average_rating(self):
        """
        Python-level calculation.
        Used if reviews are already loaded on the Product object.
        """
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    @average_rating.expression
    def average_rating(cls):
        """
        SQL-level calculation.
        Generates a correlated subquery using AVG().
        """
        from app.models.review import Review  # local import to avoid circular deps

        return (
            select(func.avg(Review.rating))
            .where(Review.product_id == cls.id)
            .label("average_rating")
        )
