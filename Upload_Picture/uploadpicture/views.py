from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import User, Img

views = Blueprint("views", __name__)

@views.route("/home")

def home():
    flash("Đăng nhập thành công !", category="success")
    current_user_id = current_user.id  # Lấy `id` của user đăng nhập hiện tại

    # Đếm số lượng ảnh mà user này đã upload
    image_count = Img.query.filter_by(user_id=current_user_id).count()

    return render_template("index.html", user = current_user, image_count=image_count)