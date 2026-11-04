import os
import uuid
from flask import abort, flash, redirect, render_template, request, url_for
from . import product_bp
from .db import (
    add_product,
    delete_product,
    get_all_products,
    get_product_by_id,
    update_product,
)
from .forms import ProductForm


def save_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    ext = os.path.splitext(file_storage.filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
    )
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_filename)
    file_storage.save(file_path)
    return f"uploads/{unique_filename}"


@product_bp.route("/")
@product_bp.route("/list")
def product_list():
    all_products = get_all_products()
    return render_template("products.html", products=all_products, title="Каталог товарів")


@product_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = ""
        if form.image.data:
            image_path = save_uploaded_image(form.image.data)

        new_product = add_product(
            name=form.name.data,
            content=form.content.data,
            price=form.price.data,
            category=form.category.data,
            quantity=form.quantity.data,
            image=image_path,
        )
        flash(f"Товар '{new_product['name']}' успішно додано!", "success")
        return redirect(url_for(".product_list"))
    elif request.method == "POST":
        flash("Помилка при додаванні товару. Перевірте поля форми.", "danger")

    return render_template("add_product.html", form=form, title="Додати товар")


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        abort(404)
    return render_template("detail_product.html", product=product, title=product["name"])


@product_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_product_by_id(product_id)
    if not product:
        abort(404)

    form = ProductForm()
    if form.validate_on_submit():
        new_image = None
        if form.image.data:
            new_image = save_uploaded_image(form.image.data)

        update_product(
            product_id=product_id,
            name=form.name.data,
            content=form.content.data,
            price=form.price.data,
            category=form.category.data,
            quantity=form.quantity.data,
            image=new_image,
        )
        flash(f"Товар '{form.name.data}' успішно оновлено!", "success")
        return redirect(url_for(".product_detail", product_id=product_id))
    elif request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = product["price"]
        form.category.data = product.get("category", "Комп'ютери")
        form.quantity.data = product.get("quantity", 1)
    elif request.method == "POST":
        flash("Помилка при оновленні товару. Перевірте поля форми.", "danger")

    return render_template(
        "edit_product.html",
        form=form,
        product=product,
        title=f"Редагувати: {product['name']}",
    )


@product_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = get_product_by_id(product_id)
    if not product:
        abort(404)

    delete_product(product_id)
    flash(f"Товар '{product['name']}' успішно видалено!", "info")
    return redirect(url_for(".product_list"))
