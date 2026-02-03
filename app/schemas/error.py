# app/schemas/error.py

from pydantic import BaseModel
from typing import Optional


class APIError(BaseModel):
    """
    Defines the standard structure for an API error response.
    """
    message: str
    code: Optional[str] = None
