import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from logic.LanguageQuizManager import Tester

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('./Data/web/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'your_secret_key'  # 用於會話管理

tester = Tester()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/languages')
def languages():
    return render_template('languages.html')

@app.route('/get_languages')
def get_languages():
    filter_text = request.args.get('filter', '').lower()
    languages_with_full_names = tester.list_languages_with_full_names()
    if filter_text:
        languages_with_full_names = [
            (code, name) for code, name in languages_with_full_names if filter_text in name.lower()
        ]
    return jsonify(languages=languages_with_full_names)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session['languages'] = request.form.getlist('languages')
    session['num_questions'] = int(request.form.get('num_questions'))
    session['difficulty'] = request.form.get('difficulty')
    session['question_type'] = request.form.get('question_type')
    tester.languages = session['languages']
    tester.generate_words_for_question(session['num_questions'])
    tester.difficulty = session['difficulty']
    session['current_question'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    current_question = session.get('current_question', 0)
    if current_question >= len(tester.questions):
        return redirect(url_for('results'))
    question = tester.questions[current_question]
    multiple_choices = tester.get_multiple_choice_question(current_question)
    return render_template('quiz.html', question=question, choices=multiple_choices, current_question=current_question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    current_question = session.get('current_question', 0)
    multiple_choice = True
    answer = request.form.get('answer')
    score = tester.check_answer(current_question, answer, multiple_choice=multiple_choice)
    session['current_question'] += 1
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    average_score = tester.get_average_score()
    standard_deviation = tester.get_standard_deviation()
    return render_template('results.html', score=tester.answers, average_score=average_score, standard_deviation=standard_deviation)

@app.route('/phoneticData/<path:filename>')
def phonetic_data(filename):
    return send_from_directory(os.path.join(app.root_path, 'Data/phoneticData'), filename)

if __name__ == '__main__':
    app.run(debug=True)
