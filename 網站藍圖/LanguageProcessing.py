from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from werkzeug.exceptions import BadRequest
import html
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
    session['current_question'] = 0
    session['correct_answers'] = 0
    session['user_answers'] = []

    # 打印或處理接收到的數據
    print(f'Selected Languages: {selected_languages}')
    print(f'Number of Questions: {num_questions}')
    print(f'Question Types: {question_types}')


    return jsonify(success=True)

@lp_bp.route('/checkanswer', methods=['POST'])
def check_answer():
    try:
        data = request.get_json()
        correct_answer = html.unescape(data.get('correctAnswer'))
        user_answer = html.unescape(data.get('userAnswer'))
        answertype = data.get('answertype')
        response_time = data.get('responsetime')

        if answertype == "multipleChoice":
            score = 100.0 if user_answer == correct_answer else 0.0

        elif answertype == "organizeLetter":
            hamming_distance = sum(1 for u, c in zip(user_answer, correct_answer) if u != c)
            length_of_correct_list = len(correct_answer)
            hamming_distance += abs(length_of_correct_list - len(user_answer))
            score = max(0, 100 - 100 * hamming_distance / length_of_correct_list)

        else:
            return jsonify({"error": "Unsupported answertype"}), 400

        # Update session with the current question's user answer and score
        current_question_index = session['current_question']
        print("index", current_question_index, answertype, data)
        if session['quiz_questions'][current_question_index]['correct_answer'] != correct_answer:
            return jsonify({"error": "Invalid answer"}), 400
        session['quiz_questions'][current_question_index]['user_answer'] = user_answer
        session['quiz_questions'][current_question_index]['percent_correct'] = score
        session['current_question'] += 1
        if response_time and type(response_time) is float:
            session['quiz_questions'][current_question_index]['response_time_seconds'] = response_time

        return jsonify({"score": score})

    except BadRequest:
        return jsonify({"error": "Invalid input format"}), 400
