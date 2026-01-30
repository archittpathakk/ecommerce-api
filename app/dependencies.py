from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close

from .database import SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, security

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(security.oauth2_scheme)
) -> models.User:
    user_id = security.decode_access_token(token)

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()

    if user is None:
        raise security.CREDENTIALS_EXCEPTION
    
    return user


def get_current_admin_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if current_user.role != "admin":
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges"
        )
    
    return current_user