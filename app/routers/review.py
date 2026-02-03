# app/routers/review.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# We need to import IntegrityError from the SQLAlchemy exceptions module
# to specifically catch the unique constraint violation.
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, dependencies

# Create a new router instance for review-related endpoints.
router = APIRouter(
    prefix="/reviews",
    tags=["Product Reviews"]
)

@router.post("/", response_model=schemas.ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: schemas.ReviewCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Create a new review for a product.

    This endpoint is protected and requires a valid JWT token.
    A user can only submit one review per product.
    """
    # 1. First, verify that the product the user is trying to review actually exists.
    product = db.query(models.Product).filter(models.Product.id == review_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {review_data.product_id} not found."
        )

   # 2. Authorization: Verify the user has purchased this product.
    # We query for an Order record associated with the current user that contains
    # an OrderItem matching the product_id.
    purchase_record = db.query(models.Order).join(models.OrderItem).filter(
        models.Order.user_id == current_user.id,
        models.OrderItem.product_id == review_data.product_id
    ).first()

    if not purchase_record:
        # If no such record is found, the user has not bought the product.
        # We raise a 403 Forbidden error, as the user is authenticated but not
        # authorized to perform this specific action.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review products you have purchased."
        )
    
    # --- END OF NEW LOGIC ---

    # 3. Create an instance of the Review model (existing logic).
    new_review = models.Review(
        **review_data.model_dump(),
        user_id=current_user.id
    )

    # 4. Handle the unique constraint for duplicate reviews (existing logic).
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already submitted a review for this product."
        )
    
    return new_review