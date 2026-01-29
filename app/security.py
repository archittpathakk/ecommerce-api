from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data (dict): The payload to include in the token (e.g., user ID).
        expires_delta (Optional[timedelta]): The lifespan of the token. Defaults to settings.

    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    
    # Set the token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use the default expiration time from settings if not provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the 'exp' (expiration) and 'iat' (issued at) claims to the payload
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    # Encode the payload into a JWT
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decodes and validates a JWT access token.

    Args:
        token (str): The JWT to decode.

    Raises:
        CREDENTIALS_EXCEPTION: If the token is invalid, expired, or has a bad signature.

    Returns:
        dict: The decoded payload from the token.
    """
    try:
        # Attempt to decode the token using the secret key and algorithm
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Handle the specific case of an expired token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        # Handle all other JWT errors (e.g., bad signature, invalid format)
        raise CREDENTIALS_EXCEPTION