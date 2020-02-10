from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
# debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def main():
    return render_template("main.html", s=satisfaction_survey)

# left off on flash messages
@app.route("/questions/<num>")
def question(num):
    # correct question number
    if int(num) == len(responses):
        question = satisfaction_survey.questions[int(num)].question
        choices = satisfaction_survey.questions[int(num)].choices
        return render_template("question.html", num=num, question=question, choices=choices)
    # survey completed redirect
    elif len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")
    # redirects when the user trys to alter the URL
    else:
        flash(
            "You're trying to access an invalid URL; these questions must be done in order.")
        return redirect(f"{len(responses)}")


@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form["answer"]
    responses.append(answer)
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"questions/{len(responses)}")
    else:
        return redirect("/complete")


@app.route("/complete")
def complete():
    return render_template("complete.html")
