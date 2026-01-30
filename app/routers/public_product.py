from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies

# Create a new APIRouter instance for public, unauthenticated endpoints.
router = APIRouter(
    
    prefix="/products",
    # We use a different tag to group these public endpoints separately in the API docs.
    tags=["Public - Products"]
)

@router.get("/", response_model=List[schemas.ProductOut])
def get_all_public_products(db: Session = Depends(dependencies.get_db)):
    products = db.query(models.product).all()

    return products