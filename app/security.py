from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.schemas.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------------------------
# Password utilities
# -------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------------------------
# Common auth exception
# -------------------------------------------------
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# -------------------------------------------------
# JWT creation
# -------------------------------------------------
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY.get_secret_value(),  # 🔐 secure access
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


# -------------------------------------------------
# JWT decoding
# -------------------------------------------------
def decode_access_token(token: str) -> str:
    """
    Decodes and validates a JWT access token, returning the user ID (sub).
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),  # 🔐 secure access
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise CREDENTIALS_EXCEPTION

        token_data = TokenData(sub=user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise CREDENTIALS_EXCEPTION

    return token_data.sub
