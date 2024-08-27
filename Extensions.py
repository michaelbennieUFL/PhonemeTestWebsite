from flask_sqlalchemy import SQLAlchemy #避免循環引用
from flask_mail import Mail
from flask_caching import Cache
from flask_login import LoginManager

資料庫 = SQLAlchemy()
郵件 = Mail()
緩存= Cache()
登錄管理器= LoginManager()