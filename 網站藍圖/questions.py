from smtpd import program

from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify

questions_bp = Blueprint("questions", __name__, url_prefix="/quiz")

@questions_bp.route("/")
def question_selector():
    return render_template("languageSelect.html")

@questions_bp.route("/quiz", methods=['GET'])
def quiz():
    if 'current_question' not in session:
        session['current_question'] = 0

    current_question_index = session['current_question']
    questions = session.get('quiz_questions', [])

    if current_question_index >= len(questions):
        return redirect(url_for('questions.quiz_results'))

    current_question = questions[current_question_index]
    question_type = current_question['question_type']

    number_of_questions = len(questions)
    total_correct = sum(answer['percent_correct'] for answer in questions if isinstance(answer['percent_correct'] ,(float,int)))
    if current_question_index > 0:
        total_correct_percent = str(int(total_correct / (current_question_index)))
    else:
        total_correct_percent = 100
    # Render the appropriate template based on the question type
    percent_done=current_question_index/number_of_questions*100
    if question_type == 'multiple_choice':
        return render_template('multipleChoice.html', **current_question, progress=percent_done, hearts=total_correct_percent)
    elif question_type == 'fill_in_the_blank':
        return render_template('fillBlank.html', **current_question, progress=percent_done, hearts=total_correct_percent)
    elif question_type == 'organize_sounds':
        return render_template('organizeLetters.html', **current_question, progress=percent_done, hearts=total_correct_percent)
    else:
        return "Unknown question type", 400

@questions_bp.route('/results')
def quiz_results():
    user_answers = session.get('quiz_questions', [])
    total_questions = len(user_answers)
    total_correct = sum(answer['percent_correct'] for answer in user_answers)

    # Calculate the overall percentage correct
    overall_percentage = total_correct / total_questions if total_questions > 0 else 0

    # Get the incorrect answers
    incorrect_answers = [answer for answer in user_answers if  answer['percent_correct']<90]
    correct_answer_amount=total_questions-len(incorrect_answers)
    return render_template('quizResults.html', user_answers=user_answers, correct_answers=correct_answer_amount, total_questions=total_questions, overall_percentage=overall_percentage, incorrect_answers=incorrect_answers)


