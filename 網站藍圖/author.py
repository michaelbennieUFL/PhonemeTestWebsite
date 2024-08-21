from flask import Blueprint, render_template

auth_bp=Blueprint("author",__name__,url_prefix="/auth")

@auth_bp.route("/login")
def login():
    return "login"

@auth_bp.route("/signup")
def signup():
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    return "logout"