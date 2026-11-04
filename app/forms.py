from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Length(min=4, max=10, message="має бути від 4 до 10 символів"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Email(message="Некоректний email"),
        ],
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Regexp(r"^\+380\d{9}$", message="Формат: +380XXXXXXXXX"),
        ],
    )
    subject = SelectField(
        "Subject",
        choices=[
            ("general", "Загальне питання"),
            ("tech", "Технічна підтримка"),
            ("cooperation", "Співпраця"),
        ],
        default="general",
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Length(max=500, message="до 500 символів"),
        ],
    )
    submit = SubmitField("Send Message")
