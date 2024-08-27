from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, NumberRange,Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    captcha = StringField('Captcha', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match.'),
        Length(min=3,message="Password must be at least 3 characters long.")
    ])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired()])
    language = SelectField('Native Language', choices=[
        ('en', '🇺🇸 English'),
        ('es', '🇪🇸 Español'),
        ('fr', '🇫🇷 Français'),
        ('zh', '🇹🇼 中文'),
        ('de', '🇩🇪 Deutsch'),
        ('ja', '🇯🇵 日本語'),
        ('ko', '🇰🇷 한국어'),
        ('ru', '🇷🇺 Русский'),
        ('it', '🇮🇹 Italiano'),
        ('pt', '🇵🇹 Português'),
        ('hi', '🇮🇳 हिन्दी'),
        ('ar', '🇸🇦 العربية'),
        ('nl', '🇳🇱 Nederlands'),
        ('sv', '🇸🇪 Svenska'),
        ('no', '🇳🇴 Norsk'),
        ('da', '🇩🇰 Dansk'),
        ('fi', '🇫🇮 Suomi'),
        ('pl', '🇵🇱 Polski'),
        ('tr', '🇹🇷 Türkçe'),
        ('he', '🇮🇱 עברית'),
        ('th', '🇹🇭 ไทย'),
        ('vi', '🇻🇳 Tiếng Việt'),
        ('id', '🇮🇩 Bahasa Indonesia'),
        ('ms', '🇲🇾 Bahasa Melayu'),
        ('el', '🇬🇷 Ελληνικά'),
        ('hu', '🇭🇺 Magyar'),
        ('cs', '🇨🇿 Čeština'),
        ('ro', '🇷🇴 Română'),
        ('sk', '🇸🇰 Slovenčina'),
        ('bg', '🇧🇬 Български'),
        ('uk', '🇺🇦 Українська'),
        ('hr', '🇭🇷 Hrvatski'),
        ('sr', '🇷🇸 Српски'),
        ('sl', '🇸🇮 Slovenščina')
    ], validators=[DataRequired()])
    age = IntegerField('Age (Optional)', validators=[Optional(), NumberRange(min=0)])
    agree_term = BooleanField('I agree to the Terms of Service', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')