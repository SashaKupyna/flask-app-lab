import logging
from flask import flash, redirect, render_template, request, url_for
from . import app
from .forms import ContactForm

logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


@app.route("/")
def main():
    return render_template("index.html", title="Головна")


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", title="Homepage", agent=agent)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/product")
def product():
    return redirect(url_for("products.product_list"))


@app.route("/contact", methods=["GET", "POST"], endpoint="contact")
@app.route("/contacts", methods=["GET", "POST"], endpoint="contacts")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger.info(
            f"Name: {form.name.data} | Email: {form.email.data} | "
            f"Phone: {form.phone.data} | Subject: {form.subject.data} | "
            f"Message: {form.message.data}"
        )
        flash("Ваше повідомлення успішно надіслано!", "success")
        return redirect(url_for("contact"))
    elif request.method == "POST":
        flash("Помилка валідації форми. Перевірте введені дані.", "danger")

    return render_template("contacts.html", form=form, title="Контакти")
