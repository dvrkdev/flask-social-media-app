# auth.py
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import UserRegistrationForm
from app.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    return "login"


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash("Ro'yxatdan o'tish muvaffaqiyatli!", "success")
        return redirect(url_for("main.home"))
    return render_template("register.html", form=form)
