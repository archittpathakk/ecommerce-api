# app/tests/test_cart.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models

# All test functions will receive fixtures like 'authenticated_client', 'test_product',
# and 'db_session' from your conftest.py file.

def test_add_item_to_cart_success(
    authenticated_client: TestClient, 
    test_product: models.Product,
    db_session: Session
):
    """
    Tests successfully adding a product to a user's initially empty cart.
    """
    # Arrange: Define the data for the item to be added.
    add_to_cart_data = {
        "product_id": test_product.id,
        "quantity": 2
    }

    # Act: Make a POST request to the endpoint to add the item.
    response = authenticated_client.post("/cart/items", json=add_to_cart_data)

    # Assert: Verify the outcome.
    # 1. Check for the correct HTTP status code. 201 Created is ideal for a new resource.
    assert response.status_code == 201

    # 2. Validate the structure and content of the response body.
    response_data = response.json()
    assert response_data["product"]["id"] == test_product.id
    assert response_data["quantity"] == add_to_cart_data["quantity"]

    # 3. (Best Practice) Verify the side effect in the database.
    #    Ensure that a Cart and a CartItem were actually created.
    user_cart = db_session.query(models.Cart).one() # We expect one cart
    assert user_cart is not None
    assert len(user_cart.items) == 1
    assert user_cart.items[0].product_id == test_product.id
    assert user_cart.items[0].quantity == add_to_cart_data["quantity"]


# app/tests/test_cart.py
# ... (keep the previous test)

def test_view_cart(authenticated_client: TestClient, test_product: models.Product):
    """
    Tests viewing the cart after an item has been added.
    """
    # Arrange: First, add an item to the cart so it's not empty.
    add_to_cart_data = {"product_id": test_product.id, "quantity": 1}
    authenticated_client.post("/cart/items", json=add_to_cart_data)

    # Act: Make a GET request to the main cart endpoint.
    response = authenticated_client.get("/cart/")

    # Assert:
    assert response.status_code == 200
    response_data = response.json()
    
    # 1. The response should contain a list of items.
    assert "items" in response_data
    assert isinstance(response_data["items"], list)
    assert len(response_data["items"]) == 1
    
    # 2. The item in the cart should match what we added.
    cart_item = response_data["items"][0]
    assert cart_item["product"]["id"] == test_product.id
    assert cart_item["quantity"] == 1
    
    # 3. Verify that the total price is calculated correctly.
    assert "total_price" in response_data
    assert float(response_data["total_price"]) == float(test_product.price)


# app/tests/test_cart.py
# ... (keep previous tests)

def test_update_cart_item_quantity(authenticated_client: TestClient, test_product: models.Product):
    """
    Tests updating the quantity of an item already in the cart.
    """
    # Arrange: Add an item with quantity 1.
    authenticated_client.post("/cart/items", json={"product_id": test_product.id, "quantity": 1})

    # Act: Make a PUT request to update the quantity to 5.
    update_data = {"quantity": 5}
    response = authenticated_client.put(f"/cart/items/{test_product.id}", json=update_data)

    # Assert:
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["product"]["id"] == test_product.id
    assert response_data["quantity"] == 5

def test_remove_item_from_cart(authenticated_client: TestClient, test_product: models.Product):
    """
    Tests removing a specific item from the cart.
    """
    # Arrange: Add an item to the cart.
    authenticated_client.post("/cart/items", json={"product_id": test_product.id, "quantity": 1})

    # Act: Make a DELETE request for that specific product.
    response = authenticated_client.delete(f"/cart/items/{test_product.id}")

    # Assert:
    # 1. A successful deletion with no content to return should be a 204 status code.
    assert response.status_code == 204
    
    # 2. Verify the cart is now empty by fetching it again.
    cart_response = authenticated_client.get("/cart/")
    assert len(cart_response.json()["items"]) == 0


# app/tests/test_cart.py
# ... (keep previous tests)

def test_clear_entire_cart(
    authenticated_client: TestClient,
    test_product: models.Product,
    test_category: models.Category,
    db_session: Session
):
    """
    Tests clearing all items from the cart at once.
    """
    # Arrange: Add multiple items to the cart.
    # Create a second product to make the test more robust.
    product2_data = models.Product(name="Second Test Product", price=50.00, stock=10, category_id=test_category.id)
    db_session.add(product2_data)
    db_session.commit()
    
    authenticated_client.post("/cart/items", json={"product_id": test_product.id, "quantity": 1})
    authenticated_client.post("/cart/items", json={"product_id": product2_data.id, "quantity": 2})

    # Act: Make a DELETE request to the root cart endpoint.
    response = authenticated_client.delete("/cart/")

    # Assert:
    assert response.status_code == 204
    
    # Verify the cart is now empty.
    cart_response = authenticated_client.get("/cart/")
    assert len(cart_response.json()["items"]) == 0
    assert float(cart_response.json()["total_price"]) == 0.0


# app/tests/test_cart.py
# ... (keep previous tests)

def test_add_more_than_available_stock_fails(
    authenticated_client: TestClient, 
    test_product: models.Product
):
    """
    Tests that a user cannot add more of an item to their cart than is available in stock.
    The 'test_product' fixture has a stock of 50.
    """
    # Arrange
    add_to_cart_data = {
        "product_id": test_product.id,
        "quantity": test_product.stock + 1  # Try to add one more than is in stock
    }

    # Act
    response = authenticated_client.post("/cart/items", json=add_to_cart_data)

    # Assert: Expect a client error, like 400 Bad Request.
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


