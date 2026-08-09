import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
USE_FIRESTORE = os.environ.get("USE_FIRESTORE", "false").lower() == "true"

db = firestore.Client(project=PROJECT_ID) if USE_FIRESTORE else None

DEMO_PRODUCTS = [
    {"id": "p1", "name": "Wireless Headphones", "description": "Bluetooth over-ear headphones with deep bass.", "price": 2499.0, "category": "Electronics", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"},
    {"id": "p2", "name": "Smart Watch", "description": "Fitness tracking, notifications and heart-rate monitoring.", "price": 3999.0, "category": "Wearables", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"},
    {"id": "p3", "name": "Running Shoes", "description": "Lightweight everyday running shoes.", "price": 2999.0, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
    {"id": "p4", "name": "Travel Backpack", "description": "Water-resistant 30L backpack for work and travel.", "price": 1799.0, "category": "Travel", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"},
    {"id": "p5", "name": "Mechanical Keyboard", "description": "Compact mechanical keyboard for developers.", "price": 3499.0, "category": "Electronics", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"},
    {"id": "p6", "name": "Coffee Mug", "description": "Minimal ceramic mug for your desk setup.", "price": 599.0, "category": "Home", "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=800"},
]

def get_products():
    if not db:
        return DEMO_PRODUCTS
    docs = db.collection("products").stream()
    products = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        products.append(item)
    return products or DEMO_PRODUCTS

def get_product(product_id):
    if not db:
        return next((p for p in DEMO_PRODUCTS if p["id"] == product_id), None)
    doc = db.collection("products").document(product_id).get()
    if not doc.exists:
        return None
    item = doc.to_dict()
    item["id"] = doc.id
    return item

def cart_items():
    cart = session.get("cart", {})
    result = []
    total = 0
    for pid, qty in cart.items():
        product = get_product(pid)
        if product:
            subtotal = product["price"] * qty
            result.append({**product, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return result, total

@app.context_processor
def inject_cart():
    return {"cart_count": sum(session.get("cart", {}).values())}

@app.route("/")
def index():
    q = request.args.get("q", "").strip().lower()
    products = get_products()
    if q:
        products = [p for p in products if q in p["name"].lower() or q in p["category"].lower()]
    return render_template("index.html", products=products, query=q)

@app.route("/product/<product_id>")
def product(product_id):
    item = get_product(product_id)
    if not item:
        return "Product not found", 404
    return render_template("product.html", product=item)

@app.post("/cart/add/<product_id>")
def add_to_cart(product_id):
    if not get_product(product_id):
        return "Product not found", 404
    cart = session.setdefault("cart", {})
    cart[product_id] = int(cart.get(product_id, 0)) + 1
    session.modified = True
    flash("Product added to cart.")
    return redirect(request.referrer or url_for("index"))

@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/update")
def update_cart():
    cart = session.setdefault("cart", {})
    for pid in list(cart.keys()):
        try:
            qty = max(0, int(request.form.get(f"qty_{pid}", 0)))
        except ValueError:
            qty = 0
        if qty == 0:
            cart.pop(pid, None)
        else:
            cart[pid] = qty
    session.modified = True
    return redirect(url_for("cart"))

@app.post("/checkout")
def checkout():
    items, total = cart_items()
    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("index"))

    customer_name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()
    if not customer_name or not email or not address:
        flash("Please complete all checkout fields.")
        return redirect(url_for("cart"))

    order = {
        "customer_name": customer_name,
        "email": email,
        "address": address,
        "items": [{"product_id": i["id"], "name": i["name"], "qty": i["qty"], "price": i["price"]} for i in items],
        "total": total,
    }

    if db:
        ref = db.collection("orders").document()
        order["order_id"] = ref.id
        ref.set(order)
    else:
        order["order_id"] = "LOCAL-DEMO"

    session["cart"] = {}
    return render_template("success.html", order=order)

@app.get("/health")
def health():
    return {"status": "ok", "firestore": bool(db)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
