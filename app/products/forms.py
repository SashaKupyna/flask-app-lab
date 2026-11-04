from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

CATEGORIES = [
    ("Комп'ютери", "Комп'ютери"),
    ("Смартфони", "Смартфони"),
    ("Планшети", "Планшети"),
    ("Аксесуари", "Аксесуари"),
    ("Електроніка", "Електроніка"),
]


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Length(min=3, message="Мінімум 3 символи"),
        ],
    )
    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Обов'язкове поле"),
        ],
        render_kw={"rows": 5, "cols": 40},
    )
    price = DecimalField(
        "Ціна ($)",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            NumberRange(min=0.01, message="Ціна має бути додатною"),
        ],
        places=2,
    )
    category = SelectField(
        "Категорія",
        choices=CATEGORIES,
        validators=[DataRequired(message="Оберіть категорію")],
    )
    quantity = IntegerField(
        "Кількість одиниць",
        validators=[
            DataRequired(message="Обов'язкове поле"),
            NumberRange(min=0, message="Кількість не може бути від'ємною"),
        ],
        default=1,
    )
    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "Дозволені тільки формати PNG, JPG, JPEG!"),
        ],
    )
    submit = SubmitField("Зберегти товар")
