from fastapi import status
from fastapi.testclient import TestClient
from app import models


def test_create_review_success(
    authenticated_client: TestClient,
    db_session,
    test_user: models.User,
    test_product: models.Product,
):
    """
    A logged-in user who has purchased a product
    should be able to leave a review.
    """

    # --- Arrange: create an order so the user is allowed to review ---
    order = models.Order(
        user_id=test_user.id,
        status=models.OrderStatus.DELIVERED,
    )
    db_session.add(order)
    db_session.flush()  # get order.id

    order_item = models.OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=1,
        price=test_product.price,
    )
    db_session.add(order_item)
    db_session.commit()

    # --- Act: submit a review ---
    review_payload = {
        "product_id": test_product.id,
        "rating": 5,
        "comment": "Amazing product!",
    }

    response = authenticated_client.post(
        "/reviews/",
        json=review_payload,
    )

    # --- Assert ---
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Amazing product!"
    assert data["product_id"] == test_product.id
    assert data["user_id"] == test_user.id
