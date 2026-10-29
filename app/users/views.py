from flask import (flash,make_response,redirect,render_template,request,session,url_for,)
from . import user_bp

VALID_USERS = {
    "admin": "123",
    "user1": "password",
    "sasha": "1234",
}


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name_formatted = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("hi.html", name=name_formatted, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for(".greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in VALID_USERS and VALID_USERS[username] == password:
            session["user"] = username
            flash("Успішний вхід в систему", "success")
            return redirect(url_for(".profile"))

        flash("Wrong data! Try again!", "danger")
        return redirect(url_for(".login"))

    if "user" in session:
        return redirect(url_for(".profile"))

    return render_template("login.html", title="Вхід")


@user_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з системи", "info")
    return redirect(url_for(".login"))


@user_bp.route("/profile")
def profile():
    if "user" not in session:
        flash("Сесія недоступна", "danger")
        return redirect(url_for(".login"))

    username = session["user"]
    theme = request.cookies.get("theme", "dark")
    cookies = request.cookies
    return render_template(
        "profile.html",
        username=username,
        theme=theme,
        cookies=cookies,
        title="Профіль",
    )


@user_bp.route("/profile/cookie/add", methods=["POST"])
def add_cookie():
    if "user" not in session:
        flash("Дії недоступні без авторизації", "danger")
        return redirect(url_for(".login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", type=int)

    if not key:
        flash("Ключ кукі порожнй", "warning")
        return redirect(url_for(".profile"))

    response = make_response(redirect(url_for(".profile")))
    if max_age and max_age > 0:
        response.set_cookie(key, value, max_age=max_age)
    else:
        response.set_cookie(key, value)

    flash(f"Кукі '{key}' успішно додано", "success")
    return response


@user_bp.route("/profile/cookie/delete", methods=["POST"])
def delete_cookie():
    if "user" not in session:
        flash("Дія недоступна без авторизації", "danger")
        return redirect(url_for(".login"))

    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ кукі для видалення", "warning")
        return redirect(url_for(".profile"))

    response = make_response(redirect(url_for(".profile")))
    response.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено", "info")
    return response


@user_bp.route("/profile/cookie/delete_all", methods=["POST"])
def delete_all_cookies():
    if "user" not in session:
        flash("Дія недоступна без авторизації", "danger")
        return redirect(url_for(".login"))

    response = make_response(redirect(url_for(".profile")))
    for key in request.cookies.keys():
        if key != "session":
            response.delete_cookie(key)

    flash("Всі користувацькі кукі успішно видалено!", "info")
    return response


@user_bp.route("/profile/theme/<string:theme_name>")
def change_theme(theme_name):
    if "user" not in session:
        return redirect(url_for(".login"))

    theme = "light" if theme_name == "light" else "dark"
    response = make_response(redirect(url_for(".profile")))
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 30)
    flash(f"Встановлено {'світлу' if theme == 'light' else 'темну'} тему", "info")
    return response
