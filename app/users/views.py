from flask import redirect, render_template, request, url_for
from . import user_bp


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name_formatted = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("hi.html", name=name_formatted, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)
