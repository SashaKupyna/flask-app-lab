import atexit
import os
from datetime import datetime
from tinydb import Query, TinyDB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "products.json")

db = TinyDB(DB_PATH)
products_table = db.table("products")

atexit.register(db.close)


def init_db():
    if len(products_table) == 0:
        initial_products = [
            {
                "id": 1,
                "name": "Laptop",
                "content": "Потужний ноутбук для навчання та роботи.",
                "price": 1200.0,
                "category": "Комп'ютери",
                "quantity": 5,
                "image": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            {
                "id": 2,
                "name": "Phone",
                "content": "Сучасний смартфон з гарною камерою.",
                "price": 800.0,
                "category": "Смартфони",
                "quantity": 10,
                "image": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            {
                "id": 3,
                "name": "PC",
                "content": "Настільний комп'ютер для ігор та роботи.",
                "price": 1800.0,
                "category": "Комп'ютери",
                "quantity": 3,
                "image": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        ]
        for item in initial_products:
            products_table.insert(item)


def get_all_products():
    init_db()
    return products_table.all()


def get_product_by_id(product_id: int):
    init_db()
    Product = Query()
    res = products_table.search(Product.id == product_id)
    return res[0] if res else None


def get_next_id():
    all_p = products_table.all()
    if not all_p:
        return 1
    return max(p.get("id", 0) for p in all_p) + 1


def add_product(name, content, price, category, quantity, image=""):
    init_db()
    new_id = get_next_id()
    new_product = {
        "id": new_id,
        "name": name,
        "content": content,
        "price": round(float(price), 2),
        "category": category,
        "quantity": int(quantity),
        "image": image,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    products_table.insert(new_product)
    return new_product


def update_product(product_id: int, name, content, price, category, quantity, image=None):
    init_db()
    Product = Query()
    existing = get_product_by_id(product_id)
    if not existing:
        return None
    updates = {
        "name": name,
        "content": content,
        "price": round(float(price), 2),
        "category": category,
        "quantity": int(quantity),
    }
    if image is not None:
        updates["image"] = image
    products_table.update(updates, Product.id == product_id)
    return get_product_by_id(product_id)


def delete_product(product_id: int):
    init_db()
    Product = Query()
    products_table.remove(Product.id == product_id)
