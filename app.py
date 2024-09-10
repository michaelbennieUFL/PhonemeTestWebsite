import os
from flask import Flask, render_template, url_for, redirect
from flask_babel import gettext
from fontTools.misc.cython import returns

import config
from Extensions import 資料庫, 郵件, 緩存, 登錄管理器, 翻譯
from models import UserModel
from 網站藍圖.questions import questions_bp
from 網站藍圖.user import user_bp
from 網站藍圖.LanguageProcessing import lp_bp
from 網站藍圖.Authenticator import auth_bp
from flask_migrate import Migrate
from TranslationHelpers import get_locale, get_timezone, supported_languages

網站 = Flask(__name__)
網站.config.from_object(config)  # 綁定配置文件
網站.secret_key = os.urandom(24)

migrate = Migrate(網站, 資料庫)
資料庫.init_app(網站)
郵件.init_app(網站)
緩存.init_app(網站)
翻譯.init_app(網站, locale_selector=get_locale, timezone_selector=get_timezone)
登錄管理器.init_app(網站)


# Inject gettext into templates
@網站.context_processor
def inject_babel():
    return dict(_=gettext)


@網站.context_processor
def inject_locale():
    return {'get_locale': get_locale}


@網站.context_processor
def inject_supported_languages():
    return dict(supported_languages=supported_languages)


# TODO: change this to the quiz select screen
登錄管理器.login_view = "user.login"


@登錄管理器.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


網站.register_blueprint(questions_bp)
網站.register_blueprint(user_bp)
網站.register_blueprint(lp_bp)
網站.register_blueprint(auth_bp)


@網站.route('/')
def hello():
    return redirect(url_for('questions.quiz'))


@網站.errorhandler(404)
def handle_404(e):
    return redirect(url_for('questions.quiz'))


if __name__ == '__main__':
    網站.run(host='0.0.0.0', port=5002)
