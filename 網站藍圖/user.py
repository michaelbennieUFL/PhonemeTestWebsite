from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, session
from Extensions import 資料庫, 緩存
from models import UserModel, QuizModel
from Forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        inputted_captcha = form.captcha.data.replace("-", "").replace("_", "").replace(" ", "")
        password = form.password.data
        language = form.language.data
        age = form.age.data if form.age.data else None  # 可選的年齡字段

        real_captcha = 緩存.get("emailCaptcha_" + email)

        # 檢查captcha是否對的
        if real_captcha != inputted_captcha:
            flash("Captcha is invalid", "danger")
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
            login_user(new_user)  # 自動登錄用戶
            flash("Registration successful! You are now logged in.", "success")
            return redirect(url_for("user.dashboard"))  # 假設你有一個儀表板頁面
        except Exception as e:
            資料庫.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserModel.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            # TODO: Make the flash work for user.dashboard
            flash("Logged in successfully.", "success")
            return redirect(url_for("user.dashboard"))  # 假設你有一個儀表板頁面
        else:
            # TODO: Make the flash work for user.login
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    # TODO: Make the flash work for user.login
    flash("You have been logged out.", "success")
    return redirect(url_for("user.login"))

@user_bp.route("/dashboard")
@login_required
def dashboard():
    # Get the last 5 quiz results
    recent_tests = QuizModel.query.filter_by(user_id=current_user.id).order_by(QuizModel.quiz_number.desc()).limit(5).all()

    # Prepare data for the chart
    labels = [f"Test {test.quiz_number}" for test in recent_tests]
    data = [test.percent_correct for test in recent_tests]

    # Get some errors
    errors = QuizModel.query.filter_by(user_id=current_user.id).filter(QuizModel.percent_correct < 100).order_by(QuizModel.quiz_number.desc()).limit(5).all()

    return render_template("dashboard.html",
                           labels=labels,
                           data=data,
                           errors=errors,
                           date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

@user_bp.route('/updateLang')
def updateLanguage():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or url_for('user.dashboard'))
