from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from Extensions import 資料庫, 緩存
from models import UserModel
from Forms import RegistrationForm

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        inputted_captcha = form.captcha.data.replace("-","").replace("_","").replace(" ","")
        password = form.password.data
        language = form.language.data
        age = form.age.data if form.age.data else None  # 可選的年齡字段

        real_captcha = 緩存.get("emailCaptcha_" + email)

        #檢查captcha是否對的
        if real_captcha != inputted_captcha:
            flash("Captcha is invalid","danger")
            return render_template("register.html", form=form)



        # 檢查電子郵件是否已經存在
        existing_user = UserModel.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Please use a different email.", "danger")
            return render_template("register.html", form=form)

        # 保存用戶到數據庫

        new_user = UserModel(username=username, email=email, password=password, mother_language=language, age=age)
        try:
            資料庫.session.add(new_user)
            資料庫.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("user.login"))
        except Exception as e:
            資料庫.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)



@user_bp.route("/login")
def login():
    return render_template("login.html")



@user_bp.route("/logout")
def logout():
    return "logout"








