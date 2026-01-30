from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # This dependency ensures that only authenticated admin users can access these endpoints.
    dependencies=[Depends(dependencies.get_current_admin_user)]
)

@router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db)):
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product.category_id} not found."
        )
    
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[schemas.ProductOut])
def get_all_products(db: Session = Depends(dependencies.get_db)):
    """
    Retrieve a list of all products. Admin access is required.
    Note: In a real-world application, you would add pagination here.
    """
    products = db.query(models.Product).all()
    return products

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Retrieve a single product by its ID. Admin access is required.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )
    return product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(dependencies.get_db)):
    
   
    product_query = db.query(models.Product).filter(models.Product.id == product_id)
    product = product_query.first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )

    
    category = db.query(models.Category).filter(models.Category.id == product_update.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product_update.category_id} not found."
        )

    
    product_query.update(product_update.model_dump(), synchronize_session=False)
    db.commit()
    
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete a product. Admin access is required.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )
    
    db.delete(product)
    db.commit()
    
    return None