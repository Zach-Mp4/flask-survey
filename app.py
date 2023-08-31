from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
app = Flask(__name__)
app.config['SECRET_KEY'] = "yurr"
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

cur_qst = 0
responses = []
cur_survey = surveys.satisfaction_survey

@app.route("/")
def start():
    global responses
    global cur_qst
    responses = []
    cur_qst = 0
    return render_template("root.html", survey = cur_survey)

@app.route("/questions/<int:num>")
def question(num):
    if int(num) > cur_qst or int(num) < cur_qst:
        flash("YOU ARE ACCESSING INVALID QUESTION")
        return redirect(f"/questions/{cur_qst}")
    return render_template("question.html", survey = cur_survey, num = num)

@app.route("/answer", methods=['POST'])
def answer():
    global cur_qst
    a = request.form.get('a')
    num = request.form.get('num')
    # responses.append(a)

    answers = session['responses']
    answers.append(a)
    session['responses'] = answers

    if int(num) == len(cur_survey.questions) - 1:
        return redirect("/thanks")
    cur_qst = cur_qst + 1
    return redirect(f"/questions/{cur_qst}")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route("/submit", methods=["POST"])
def submit():
    session["responses"] = []
    return redirect("/questions/0")
