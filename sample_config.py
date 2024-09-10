
#Database
HOSTNAME="127.0.0.1"
SQLPORT=3306
USERNAME="{Username}"
PASSWORD="{Username}"
DATABASE ="{DataBaseName}"
SQLALCHEMY_DATABASE_URI= f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{SQLPORT}/{DATABASE}?charset=utf8"



#Caching

CACHE_TYPE='simple'
CACHE_DEFAULT_TIMEOUT=5*60# 5 minutes
CACHE_KEY_PREFIX="app_cache"

#Mailing

MAIL_SERVER="{mail server}"
MAIL_PORT=587
MAIL_USE_TLS=True   # May have to change depending on your provider
MAIL_USE_SSL=False
MAIL_USERNAME="{email}"
MAIL_PASSWORD="{password}"
MAIL_DEFAULT_SENDER="{email}"


#Translations

BABEL_DEFAULT_LOCALE = 'en'
BABEL_TRANSLATION_DIRECTORIES = './translations'
