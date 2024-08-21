from Extensions import 資料庫
from datetime import datetime


class UserModel(資料庫.Model):
    __tablename__ = "user"
    id = 資料庫.Column(資料庫.Integer, primary_key=True, autoincrement=True)
    username = 資料庫.Column(資料庫.String(63),nullable=False)
    password = 資料庫.Column(資料庫.String(63),nullable=False)
    email = 資料庫.Column(資料庫.String(63),nullable=False,unique=True)
    join_time =資料庫.Column(資料庫.DateTime,default=datetime.now())
    mother_language = 資料庫.Column(資料庫.String(63),nullable=False)

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