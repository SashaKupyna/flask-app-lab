from flask import abort, render_template
from . import product_bp

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "ноутбук для навчання та роботи",
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "сучасний смартфон ",
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп'ютер",
    },
]


@product_bp.route("/")
def product_list():
    return render_template("products.html", products=products, title="Каталог товарів")


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    for item in products:
        if item["id"] == product_id:
            return render_template("detail_product.html", product=item, title=item["name"])
    abort(404)
