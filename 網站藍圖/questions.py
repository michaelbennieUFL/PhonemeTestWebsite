from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify

questions_bp = Blueprint("questions", __name__, url_prefix="/")

@questions_bp.route("/")
def question_selector():
    return render_template("languageSelect.html")

@questions_bp.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session:
        session['current_question'] = 0
        session['correct_answers'] = 0
        session['user_answers'] = []

    current_question_index = session['current_question']
    questions = session.get('quiz_questions', [])

    if current_question_index >= len(questions):
        return redirect(url_for('questions.quiz_results'))

    current_question = questions[current_question_index]
    question_type = current_question['question_type']

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = current_question['correct_answer']

        # Store the user answer and check correctness
        session['user_answers'].append({
            'question': current_question,
            'user_answer': user_answer,
            'is_correct': user_answer == correct_answer
        })

        if user_answer == correct_answer:
            session['correct_answers'] += 1

        # Move to the next question
        session['current_question'] += 1
        return redirect(url_for('questions.start_quiz'))

    # Render the appropriate template based on the question type
    if question_type == 'multiple_choice':
        return render_template('multipleChoice.html', **current_question)
    elif question_type == 'fill_in_the_blank':
        return render_template('fillBlank.html', **current_question)
    elif question_type == 'organize_sounds':
        return render_template('organizeLetters.html', **current_question)
    else:
        return "Unknown question type", 400

@questions_bp.route('/results')
def quiz_results():
    user_answers = session.get('user_answers', [])
    correct_answers = session.get('correct_answers', 0)
    total_questions = len(user_answers)

    return render_template('quizResults.html', user_answers=user_answers, correct_answers=correct_answers, total_questions=total_questions)
