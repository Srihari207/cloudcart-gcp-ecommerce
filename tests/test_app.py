import os

os.environ["USE_FIRESTORE"] = "false"

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