# main.py
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import PostForm
from app.models import Post

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post muvaffaqiyatli yaratildi!", "success")
        return redirect(url_for("main.home"))
    return render_template("home.html", form=form, posts=posts)
