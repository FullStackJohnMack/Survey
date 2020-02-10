from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

RESPONSES_KEY = "responses"


@app.route("/")
def main():
    return render_template("main.html", s=satisfaction_survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def answer():
    """Handles when a question is answered and adds to session."""
    answer = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    # if routes user to next question
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"questions/{len(responses)}")
    # else redirects to "thank you" page upon completion of survey
    else:
        return redirect("/complete")


@app.route("/questions/<num>")
def question(num):
    """Handles a what question comes next."""
    responses = session.get(RESPONSES_KEY)
    # returns page for correct next question
    if int(num) == len(responses):
        question = satisfaction_survey.questions[int(num)].question
        choices = satisfaction_survey.questions[int(num)].choices
        return render_template("question.html", num=num, question=question, choices=choices)
    # returns survey complete page
    elif len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")
    # returns redirects to correct page if the user trys to alter the URL
    else:
        flash(
            "You're trying to access an invalid URL; these questions must be done in order.")
        return redirect(f"{len(responses)}")


@app.route("/complete")
def complete():
    """Handles return of complete page."""
    return render_template("complete.html")
