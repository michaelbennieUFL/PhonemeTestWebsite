from flask import Blueprint, render_template

user_bp=Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/login")
def login():
    return render_template("login.html")

@user_bp.route("/signup")
def signup():
    return render_template("register.html")


@user_bp.route("/logout")
def logout():
    return "logout"