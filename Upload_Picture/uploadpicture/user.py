from flask import Blueprint, render_template, request, flash, session, redirect, url_for, Response
from .models import User, Img
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
user = Blueprint("user", __name__)


@user.route("/login", methods = ["GET", "POST"])
@user.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        user = User.query.filter_by(Name = user_name).first()
        if user:
            
            if check_password_hash(user.Password, password):
                # session["user"] = user_name
                # session.permanent = True
                login_user(user, remember=True)
                flash("Đăng nhập thành công!", category="success")
                
                return redirect(url_for("views.home"))
            else:
                flash("Sai mật khẩu, thử lại!", category="error")
        else:
            flash("Người dùng không tồn tại!", category="error")
    return render_template("login.html", user = current_user)

@user.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")


        user = User.query.filter_by(Name = user_name).first()
        if user:
            flash("Tên này đã tồn tại", category="error")
        elif len(user_name) < 8:
            flash("Tên phải hơn 8 ký tự",category="error")
        elif len(password) < 6:
            flash("Mật khẩu phải hơn 6 ký tự",category="error")
        elif password != confirm_password:
            flash("Mật khẩu chưa khớp. Nhập lại !",category="error")
        else:
            password = generate_password_hash(password)
            new_user = User(user_name, password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Đăng ký thành công",category="success")
                login_user(user, remember= True)
                return redirect(url_for("views.html"))
            except:
                "error"
    
    return render_template("signup.html", user = current_user)

@user.route("/logout")
@login_required
def logout():
    # if "user" in session:
    #     session.pop("user", None)
    #     flash("Đăng xuất thành công")
    # else:
    #     flash("Cần đăng nhập!")
    # return redirect(url_for("user.login"))
    logout_user()  # Đăng xuất user khỏi Flask-Login
    flash("Đã đăng xuất thành công!", category="success")
    return redirect(url_for("user.login"))

@user.route('/upload', methods=['POST'])
@login_required
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400
    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    return 'Img Uploaded!', 200

@user.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)