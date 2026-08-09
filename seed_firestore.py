import os
from google.cloud import firestore

db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

products = [
    {"name": "Wireless Headphones", "description": "Bluetooth over-ear headphones with deep bass.", "price": 2499.0, "category": "Electronics", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"},
    {"name": "Smart Watch", "description": "Fitness tracking, notifications and heart-rate monitoring.", "price": 3999.0, "category": "Wearables", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"},
    {"name": "Running Shoes", "description": "Lightweight everyday running shoes.", "price": 2999.0, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
    {"name": "Travel Backpack", "description": "Water-resistant 30L backpack for work and travel.", "price": 1799.0, "category": "Travel", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"},
    {"name": "Mechanical Keyboard", "description": "Compact mechanical keyboard for developers.", "price": 3499.0, "category": "Electronics", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"},
    {"name": "Coffee Mug", "description": "Minimal ceramic mug for your desk setup.", "price": 599.0, "category": "Home", "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=800"},
]

for i, product in enumerate(products, 1):
    db.collection("products").document(f"p{i}").set(product)

print("Seeded products successfully.")
