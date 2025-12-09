from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models import User


class UserRegistrationForm(FlaskForm):
    username = StringField(
        "Foydalanuvchi nomi", validators=[DataRequired(), Length(min=5, max=64)]
    )
    password = PasswordField("Parol", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Hisob yaratish")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Bu foydalanuvchi nomi allaqachon band. Iltimos, boshqasini tanlang."
            )
