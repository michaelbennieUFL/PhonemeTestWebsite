from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, send_from_directory

from logic.DataHandler import SingleWordDataHandler
from logic.LanguageQuizManager import Tester

lp_bp=Blueprint("lp", __name__, url_prefix="/languages")

tester = Tester(SingleWordDataHandler())

@lp_bp.route('/get_languages')
def get_languages():
    filter_text = request.args.get('filter', '').lower()
    languages_with_full_names = tester.list_languages_with_full_names()
    if filter_text:
        languages_with_full_names = [
            (code, name) for code, name in languages_with_full_names if filter_text in name.lower()
        ]
    return jsonify(languages=languages_with_full_names)

@lp_bp.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    # 從 POST 請求中接收數據
    selected_languages = request.form.getlist('languages[]')  # 這裡用 getlist 因為 languages 是個列表
    num_questions = request.form.get('num_questions', type=int)
    question_types = request.form.getlist('question_types[]')  # 同樣是個列表

    # 生成問題
    generated_questions = tester.generate_questions(
        selected_languages=selected_languages,
        number=num_questions,
        question_types=question_types
    )

    # 將生成的問題存儲到 session 中
    session['quiz_questions'] = generated_questions

    # 打印或處理接收到的數據
    print(f'Selected Languages: {selected_languages}')
    print(f'Number of Questions: {num_questions}')
    print(f'Question Types: {question_types}')

    return jsonify(success=True)