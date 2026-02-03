import pytest
import uuid
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.main import app
from app.security import hash_password
from app.dependencies import get_db
from app.database_test import (
    TestingSessionLocal,
    create_test_database,
    drop_test_database,
)


# -------------------------------------------------------------------
# Database lifecycle
# -------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    create_test_database()
    yield
    drop_test_database()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Provides a fully isolated database session for each test
    using a rollback-only transaction.
    """
    connection = TestingSessionLocal().bind.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()



# -------------------------------------------------------------------
# Users
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_user(db_session: Session) -> models.User:
    user = models.User(
        email=f"testuser_{uuid.uuid4()}@example.com",
        hashed_password=hash_password("password123"),
        role="customer",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_user(db_session: Session) -> models.User:
    admin = models.User(
        email=f"admin_{uuid.uuid4()}@example.com",
        hashed_password=hash_password("adminpassword"),
        role="admin",
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


# -------------------------------------------------------------------
# Authenticated clients 
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def authenticated_client(
    db_session: Session, test_user: models.User
) -> Generator[TestClient, None, None]:

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "password123",
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_authenticated_client(
    db_session: Session, admin_user: models.User
) -> Generator[TestClient, None, None]:

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/users/login",
        data={
            "username": admin_user.email,
            "password": "adminpassword",
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client

    app.dependency_overrides.clear()


# -------------------------------------------------------------------
# Catalog
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_category(db_session: Session) -> models.Category:
    category = models.Category(
        name=f"Test Category {uuid.uuid4()}"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture(scope="function")
def test_product(
    db_session: Session,
    test_category: models.Category,
) -> models.Product:
    product = models.Product(
        name="Test Product",
        description="A product for testing",
        price=99.99,
        stock=10,
        category_id=test_category.id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
