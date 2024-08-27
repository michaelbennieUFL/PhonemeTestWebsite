import string
import random
import time
from flask import Blueprint, render_template, request, jsonify
from flask_mail import Message
from Extensions import 資料庫, 郵件, 緩存


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/captcha/email")
def get_captcha():
    target_email = request.args.get("email")
    username = request.args.get("username")

    if not target_email or not username:
        return jsonify({"code": 400, "message": "Missing username or email", "data": None}), 400

    # 檢查是否已經在過去3分鐘內發送過驗證碼
    last_sent_time = 緩存.get("emailCaptchaTime_" + target_email)
    current_time = time.time()

    if last_sent_time and (current_time - last_sent_time) < 1*60:
        return jsonify({"code": 429, "message": "Captcha already sent, please wait", "data": None}), 429

    # 生成驗證碼
    source_digits = string.digits * 5
    captcha = random.sample(source_digits, 6)
    user_readable_captcha = "".join(captcha[0:3]) + "-" + "".join(captcha[3:])

    print("captcha:", captcha, user_readable_captcha)

    try:
        # 渲染模板並發送郵件
        message = Message(
            "註冊驗證碼",
            recipients=[target_email],
            html=render_template(
                "emailVerification.html",
                Username=username,
                OTP_PASSWORD=user_readable_captcha,
                TARGET_ADRESS=target_email
            )
        )

        # 發送郵件
        郵件.send(message)

        # 將驗證碼和發送時間存儲在緩存中
        緩存.set("emailCaptcha_" + target_email, "".join(captcha), timeout=5*60)  # 設置5分鐘過期
        緩存.set("emailCaptchaTime_" + target_email, current_time)

        return jsonify({"code": 200, "message": "Code Sent", "data": None}), 200

    except Exception as e:
        return jsonify({"code": 500, "message": "Message was unable to be sent", "data": {"details": str(e)}}), 500


@auth_bp.route("/captcha/check")
def check_captcha():
    target_email = request.args.get("email")
    captcha= 緩存.get("emailCaptcha"+target_email)
    if not captcha:
        return "失敗了"
    return captcha

