import os
import sys

os.environ["USE_FIRESTORE"] = "false"

# Add project root to Python import path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app


def test_homepage():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"CloudCart" in response.data


def test_product_page():
    client = app.test_client()

    response = client.get("/product/p1")

    assert response.status_code == 200
    assert b"Wireless Headphones" in response.data


def test_cart_page():
    client = app.test_client()

    response = client.get("/cart")

    assert response.status_code == 200


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_add_to_cart():
    client = app.test_client()

    response = client.post(
        "/cart/add/p1",
        follow_redirects=True
    )

    assert response.status_code == 200

def test_login_page():
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page():
    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200
    assert b"Register" in response.data


def test_auth_verify_without_token():
    client = app.test_client()

    response = client.post("/api/auth/verify")

    assert response.status_code == 401
    assert response.json["authenticated"] is False


def test_my_orders_without_token():
    client = app.test_client()

    response = client.get("/my-orders")

    assert response.status_code == 401


def test_order_details_without_token():
    client = app.test_client()

    response = client.get("/my-orders/test-order-id")

    assert response.status_code == 401
