from collections import defaultdict
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
            print(e)
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
    recent_tests = QuizModel.query.filter_by(user_id=current_user.id).order_by(QuizModel.quiz_number.desc()).limit(200).all()

    quiz_numbers = [test.quiz_number for test in recent_tests]

    all_questions = QuizModel.query.filter(QuizModel.user_id == current_user.id, QuizModel.quiz_number.in_(quiz_numbers)).order_by(QuizModel.quiz_number.desc(), QuizModel.question_number).all()

    if all_questions is not None and len(all_questions) > 0:
        all_questions.reverse()

    quiz_data = defaultdict(list)

    for quiz in all_questions:
        quiz_data[quiz.quiz_number].append(quiz.percent_correct)

    labels = [f"Test {quiz_number}" for quiz_number in quiz_data.keys()]
    data = [sum(scores) / len(scores) for scores in quiz_data.values()]

    errors = [quiz for quiz in all_questions if quiz.percent_correct < 100]

    # Example highlight languages, this could be generated dynamically based on the user or test data
    highlight_languages = [
        ['ady', 'Adyghe', 0.5],
        ['aka', 'Akan', 0.8],
        ['am', 'Amharic', 0.5],
        ['hak', 'Hakka', 0.3],
        ['nan', 'Min Nan', 0.3]
    ]

    return render_template("dashboard.html",
                           labels=labels,
                           data=data,
                           errors=errors,
                           highlight_languages=highlight_languages,
                           date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


@user_bp.route('/updateLang')
def updateLanguage():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or url_for('user.dashboard'))
