from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app import security


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(security.oauth2_scheme),
) -> User:
    # ✅ Use YOUR existing decode function
    user_id = security.decode_access_token(token)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise security.CREDENTIALS_EXCEPTION

    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges",
        )

    return current_user
