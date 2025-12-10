# auth.py
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, UserRegistrationForm
from app.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Qaytib kelganingizdan xursandmiz!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Noto'g'ri foydalanuvchi nomi yoki parol", "danger")
    return render_template("login.html", form=form)


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


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Siz tizimdan chiqdingiz.", "info")
    return redirect(url_for("auth.login"))
