
#Database
HOSTNAME="127.0.0.1"
SQLPORT=3306
USERNAME="root"
PASSWORD=""
DATABASE ="phonemetestwebsite"
SQLALCHEMY_DATABASE_URI= f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{SQLPORT}/{DATABASE}?charset=utf8"



#Caching

CACHE_TYPE='simple'
CACHE_DEFAULT_TIMEOUT=5*60# 5 minutes
CACHE_KEY_PREFIX="app_cache"

#Mailing

MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME="phonemiclearning@gmail.com"
MAIL_PASSWORD="bdxa ehjn fbuq pwko"
MAIL_DEFAULT_SENDER="phonemiclearning@gmail.com"


#Translations

BABEL_DEFAULT_LOCALE = 'en'
BABEL_TRANSLATION_DIRECTORIES = './translations'