import os

from flask import Flask, render_template
from fontTools.misc.cython import returns

import config
from Extensions import 資料庫,郵件,緩存,登錄管理器,翻譯
from models import UserModel
from 網站藍圖.questions import questions_bp
from 網站藍圖.user import user_bp
from 網站藍圖.LanguageProcessing import lp_bp
from 網站藍圖.Authenticator import auth_bp
from flask_migrate import Migrate

網站 = Flask(__name__)
網站.config.from_object(config) #綁定配置文件
網站.secret_key=os.urandom(24)

migrate = Migrate(網站,資料庫)
資料庫.init_app(網站)
郵件.init_app(網站)
緩存.init_app(網站)
翻譯.init_app(網站)
登錄管理器.init_app(網站)
# TODO: change this to the quiz select screen
登錄管理器.login_view="user.login"

@登錄管理器.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


網站.register_blueprint(questions_bp)
網站.register_blueprint(user_bp)
網站.register_blueprint(lp_bp)
網站.register_blueprint(auth_bp)




if __name__ == '__main__':
    網站.run()
