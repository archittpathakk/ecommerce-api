# app/routers/category.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies

# Create a new router instance for category-related endpoints.
router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    # Apply the admin-check dependency to every endpoint in this router.
    # This is a powerful way to secure an entire section of your API.
    dependencies=[Depends(dependencies.get_current_admin_user)]
)

# --- CREATE (POST) ---
@router.post("/", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(dependencies.get_db)):
    """
    Create a new product category. Admin access is required.
    """
    # Check if a category with the same name already exists to prevent duplicates.
    existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category.name}' already exists."
        )
    
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# --- READ ALL (GET) ---
@router.get("/", response_model=List[schemas.CategoryOut])
def get_all_categories(db: Session = Depends(dependencies.get_db)):
    """
    Retrieve a list of all product categories. Admin access is required.
    """
    categories = db.query(models.Category).all()
    return categories

# --- READ ONE (GET by ID) ---
@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category_by_id(category_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Retrieve a single product category by its ID. Admin access is required.
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found."
        )
    return category

# --- UPDATE (PUT) ---
@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category_update: schemas.CategoryCreate, db: Session = Depends(dependencies.get_db)):
    """
    Update the name of an existing product category. Admin access is required.
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found."
        )
    
    # Check if the new name is already taken by another category.
    existing_category_with_new_name = db.query(models.Category).filter(models.Category.name == category_update.name).first()
    if existing_category_with_new_name and existing_category_with_new_name.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category_update.name}' already exists."
        )
        
    category.name = category_update.name
    db.commit()
    db.refresh(category)
    return category

# --- DELETE (DELETE) ---
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete a product category. Admin access is required.
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found."
        )
    
    db.delete(category)
    db.commit()
    # A 204 response should not have a body, so we return None.
    return None
