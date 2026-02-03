# app/tests/test_utils.py

import pytest
from jose import JWTError
from fastapi import HTTPException

from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


# -------------------------------------------------
# Password hashing tests
# -------------------------------------------------
def test_hash_password():
    password = "plain_password"
    hashed = hash_password(password)

    assert hashed is not None
    assert isinstance(hashed, str)
    assert hashed != password


def test_verify_password():
    password = "mysecretpassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


# -------------------------------------------------
# JWT tests
# -------------------------------------------------
def test_create_and_decode_access_token():
    data = {"sub": "test_user_id"}

    token = create_access_token(data)

    decoded_sub = decode_access_token(token)

    assert decoded_sub == data["sub"]


def test_decode_invalid_token():
    invalid_token = "this.is.not.a.valid.token"

    with pytest.raises(HTTPException) as exc:
        decode_access_token(invalid_token)

    assert exc.value.status_code == 401
