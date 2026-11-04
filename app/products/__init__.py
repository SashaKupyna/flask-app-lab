from flask import Blueprint

product_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    template_folder="templates/products",
    static_folder="static",
)

from . import views
