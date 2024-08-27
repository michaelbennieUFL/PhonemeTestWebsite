from Extensions import 資料庫
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserModel(資料庫.Model, UserMixin):
    __tablename__ = "user"
    id = 資料庫.Column(資料庫.Integer, primary_key=True, autoincrement=True)
    username = 資料庫.Column(資料庫.String(63), nullable=False)
    password_hash = 資料庫.Column(資料庫.String(162), nullable=False)
    email = 資料庫.Column(資料庫.String(63), nullable=False, unique=True)
    join_time = 資料庫.Column(資料庫.DateTime, default=datetime.now())
    mother_language = 資料庫.Column(資料庫.String(63), nullable=False)
    age = 資料庫.Column(資料庫.Integer, nullable=True)

    def __init__(self, username, email, password, mother_language, age=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.mother_language = mother_language
        self.age = age

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class QuizModel(資料庫.Model):
    __tablename__ = "quiz"
    id = 資料庫.Column(資料庫.Integer, primary_key=True, autoincrement=True)
    quiz_number = 資料庫.Column(資料庫.Integer, nullable=False)
    question_number = 資料庫.Column(資料庫.Integer, nullable=False)
    question_type = 資料庫.Column(資料庫.String(63), nullable=False)
    language = 資料庫.Column(資料庫.String(63), nullable=False)
    answer = 資料庫.Column(資料庫.String(255), nullable=False)
    user_answer = 資料庫.Column(資料庫.String(255))

    # 關聯到UserModel
    user_id = 資料庫.Column(資料庫.Integer, 資料庫.ForeignKey('user.id'), nullable=True)
    user = 資料庫.relationship('UserModel', backref=資料庫.backref('quizzes', lazy=True))

    __table_args__ = (
        資料庫.UniqueConstraint('quiz_number', 'question_number', name='uq_quiz_question'),
    )