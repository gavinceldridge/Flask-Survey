from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
survey = satisfaction_survey
responses = []


@app.route('/')
def home():
    """Show the home directory"""
    return render_template('index.html', survey=satisfaction_survey)


@app.route('/thanks')
def thanks():
    """Thank user after survey completion"""
    return render_template('thanks.html')


@app.route('/question/<int:question_num>')
def question(question_num):
    """Show the survey question at question_num"""
    if len(responses) == len(satisfaction_survey.questions):
        flash('You already completed the survey!')
        return redirect('/thanks')
    elif question_num != len(responses):
        flash('Please complete the survey in order!')
        return redirect(f'/question/{len(responses)}')
    return render_template('question.html', survey=satisfaction_survey, num=question_num)


@app.route("/answer/<answer_num>", methods=["POST"])
def answer(answer_num):
    """For answering a question form and redirecting to the next question"""
    response = request.form['question']
    responses.append(response)
    if int(answer_num) < len(survey.questions)-1:
        return redirect(f"/question/{int(answer_num)+1}")
    return redirect('/thanks')
