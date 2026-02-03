from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models


def test_create_order_success(
    authenticated_client: TestClient,
    test_product: models.Product,
    db_session: Session,
):
    """
    Happy path: cart → order → stock reduced → cart cleared
    """
    initial_stock = test_product.stock
    order_quantity = 2

    # Add item to cart
    response = authenticated_client.post(
        "/cart/items",
        json={"product_id": test_product.id, "quantity": order_quantity},
    )
    assert response.status_code == 201

    # Create order
    response = authenticated_client.post("/orders/")
    assert response.status_code == 201

    order_data = response.json()
    assert order_data["status"] == "pending"
    assert len(order_data["items"]) == 1
    assert order_data["items"][0]["quantity"] == order_quantity

    # Stock reduced
    db_session.refresh(test_product)
    assert test_product.stock == initial_stock - order_quantity

    # Order exists
    order_in_db = db_session.query(models.Order).first()
    assert order_in_db is not None
    assert len(order_in_db.items) == 1

    # Cart cleared
    cart_response = authenticated_client.get("/cart/")
    assert cart_response.status_code == 200
    assert cart_response.json()["items"] == []


def test_create_order_with_empty_cart_fails(
    authenticated_client: TestClient,
):
    response = authenticated_client.post("/orders/")
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_create_order_insufficient_stock_fails(
    authenticated_client: TestClient,
    test_product: models.Product,
    db_session: Session,
):
    product_id = test_product.id
    order_quantity = test_product.stock

    # Add item to cart
    authenticated_client.post(
        "/cart/items",
        json={"product_id": product_id, "quantity": order_quantity},
    )

    # Simulate race condition
    product = (
        db_session.query(models.Product)
        .filter(models.Product.id == product_id)
        .one()
    )
    product.stock = order_quantity - 1
    db_session.commit()

    # Attempt checkout
    response = authenticated_client.post("/orders/")
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()

    assert db_session.query(models.Order).count() == 0



def test_get_user_orders_success(
    authenticated_client: TestClient,
    test_product: models.Product,
):
    authenticated_client.post(
        "/cart/items",
        json={"product_id": test_product.id, "quantity": 1},
    )
    authenticated_client.post("/orders/")

    response = authenticated_client.get("/orders/")
    assert response.status_code == 200

    orders = response.json()
    assert len(orders) == 1
    assert orders[0]["items"][0]["product"]["id"] == test_product.id


def test_user_cannot_access_other_users_order(
    authenticated_client: TestClient,
    admin_authenticated_client: TestClient,
    test_product: models.Product,
):
    admin_authenticated_client.post(
        "/cart/items",
        json={"product_id": test_product.id, "quantity": 1},
    )
    order_response = admin_authenticated_client.post("/orders/")
    admin_order_id = order_response.json()["id"]

    response = authenticated_client.get(f"/orders/{admin_order_id}")
    assert response.status_code == 403
