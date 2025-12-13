from flask_wtf import FlaskForm
from python_usernames import is_safe_username
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


class UserRegistrationForm(FlaskForm):
    name = StringField("Ism", validators=[DataRequired(), Length(max=64)])
    username = StringField(
        "Foydalanuvchi nomi", validators=[DataRequired(), Length(min=5, max=64)]
    )
    password = PasswordField("Parol", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Hisob yaratish")

    def validate_username(self, username):
        if not is_safe_username(username.data):
            raise ValidationError(
                "Ushbu foydalanuvchi nomidan foydalanishga ruxsat berilmaydi."
            )
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Bu foydalanuvchi nomi allaqachon band. Iltimos, boshqasini tanlang."
            )


class PostForm(FlaskForm):
    content = TextAreaField(
        "Post tarkibi", validators=[DataRequired(), Length(max=300)]
    )
    submit = SubmitField("Yaratish")


class LoginForm(FlaskForm):
    username = StringField(
        "Foydalanuvchi nomi", validators=[DataRequired(), Length(min=5, max=64)]
    )
    password = PasswordField("Parol", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Kirish")
