# app/tests/test_user_auth.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models


def test_register_user_success(client: TestClient, db_session: Session):
    """
    Tests the successful registration of a new user.
    """
    user_data = {
        "email": "newuser@example.com",
        "password": "strongpassword123"
    }

    response = client.post("/users/register", json=user_data)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["email"] == user_data["email"]
    assert response_data["role"] == "customer"
    assert "id" in response_data
    assert "hashed_password" not in response_data

    # Verify user exists in DB
    db_user = db_session.query(models.User).filter_by(email=user_data["email"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]


def test_register_user_duplicate_email(client: TestClient, test_user: models.User):
    """
    Tests that registering with an existing email fails.
    """
    duplicate_user_data = {
        "email": test_user.email,
        "password": "anotherpassword"
    }

    response = client.post("/users/register", json=duplicate_user_data)

    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_login_user_success(client: TestClient, test_user: models.User):
    """
    Tests successful login with correct credentials.
    """
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }

    response = client.post("/users/login", data=login_data)

    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


def test_login_user_incorrect_password(client: TestClient, test_user: models.User):
    """
    Tests login failure with incorrect password.
    """
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }

    response = client.post("/users/login", data=login_data)

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_get_current_user_success(authenticated_client: TestClient, test_user: models.User):
    """
    Tests accessing /users/me with a valid token.
    """
    response = authenticated_client.get("/users/me")

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["email"] == test_user.email
    assert response_data["id"] == test_user.id
    assert "hashed_password" not in response_data


def test_get_current_user_no_token(client: TestClient):
    """
    Tests accessing /users/me without authentication.
    """
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
