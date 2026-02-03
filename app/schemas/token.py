# app/schemas/token.py

from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents the structure of the JWT access token response.
    """
    access_token: str
    # The 'token_type' field indicates how the token should be used in the
    # Authorization header. "bearer" is the standard for JWTs.
    token_type: str

class TokenData(BaseModel):
    """
    Represents the data (payload) stored inside the JWT.
    """
    # The 'sub' (subject) claim in a JWT is typically used to store the user's identifier.
    # We expect this to be the user's ID, which is a string in our token creation logic.
    sub: str | None = None