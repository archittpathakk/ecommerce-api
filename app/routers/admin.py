from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserOut
from app.dependencies import get_db, get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(get_current_admin_user)],
)

@router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieves a list of all users in the system.
    This endpoint is protected and only accessible by users with the 'admin' role.
    """
    return db.query(User).all()
