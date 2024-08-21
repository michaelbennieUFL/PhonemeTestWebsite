import os

from flask import Flask, render_template
import config
from Extensions import 資料庫
import models
from 網站藍圖.questions import questions_bp
from 網站藍圖.user import user_bp
from 網站藍圖.LanguageProcessing import lp_bp
from models import UserModel
from flask_migrate import Migrate

網站 = Flask(__name__)
網站.config.from_object(config) #綁定配置文件
網站.secret_key=os.urandom(24)

migrate = Migrate(網站,資料庫)
資料庫.init_app(網站)
網站.register_blueprint(questions_bp)
網站.register_blueprint(user_bp)
網站.register_blueprint(lp_bp)


@網站.route('/a')
def index():
    return render_template('pageTemplate.html')


if __name__ == '__main__':
    網站.run()
