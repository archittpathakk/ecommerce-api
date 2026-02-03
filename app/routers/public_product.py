from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional

from .. import models, schemas, dependencies
from app.schemas.error import APIError


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# -------------------------------------------------
# GET all products (public)
# -------------------------------------------------
@router.get(
    "/",
    response_model=List[schemas.ProductOut],
    summary="Get All Products",
)
def get_all_public_products(
    db: Session = Depends(dependencies.get_db),
    category_id: Optional[int] = Query(
        default=None,
        description="Filter products by category ID"
    ),
    q: Optional[str] = Query(
        default=None,
        description="Search for product name or description"
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="The number of items to skip"
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=250,
        description="The maximum number of items to return"
    ),
):
    """
    Retrieves a list of all publicly available products.

    Supports optional filtering by category, search queries,
    and pagination.
    """
    query_db = db.query(models.Product)

    if category_id is not None:
        query_db = query_db.filter(models.Product.category_id == category_id)

    if q is not None:
        search_term = f"%{q}%"
        query_db = query_db.filter(
            or_(
                models.Product.name.ilike(search_term),
                models.Product.description.ilike(search_term),
            )
        )

    products = query_db.offset(skip).limit(limit).all()
    return products


# -------------------------------------------------
# GET product by ID (public)
# -------------------------------------------------
@router.get(
    "/{product_id}",
    response_model=schemas.ProductOut,
    summary="Get a Single Product by ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": APIError,
            "description": "The product with the specified ID was not found.",
        }
    },
)
def get_public_product_by_id(
    product_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Retrieves the complete details for a specific product.

    Includes:
    - Category information
    - All associated reviews

    Errors:
    - 404 Not Found if the product does not exist
    """
    product = (
        db.query(models.Product)
        .options(
            joinedload(models.Product.category),
            joinedload(models.Product.reviews),
        )
        .filter(models.Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )

    return product


# -------------------------------------------------
# GET reviews for a product (public)
# -------------------------------------------------
@router.get(
    "/{product_id}/reviews",
    response_model=List[schemas.ReviewOut],
    summary="Get Reviews for a Product",
)
def get_reviews_for_product(
    product_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Retrieves all reviews for a specific product.

    This is a public endpoint and does not require authentication.

    Errors:
    - 404 Not Found if the product does not exist
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )

    return product.reviews
