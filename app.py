from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime
import json

app = Flask(__name__)

# Simple "database" (since you only need 1 user)
user_data = {
    "start_time": None,
    "formations_visited": [],
    "answers": []
}

question_to_formation = {
    "1": "4231",
    "2": "433",
    "3": "532",
    "4": "41212",
    "5": "4231"
}

# ----------------------
# HOME PAGE
# ----------------------
@app.route("/")
def home():
    return render_template("home.html")


# ----------------------
# START BUTTON TRACKING
# ----------------------
@app.route("/start", methods=["POST"])
def start():
    user_data["start_time"] = str(datetime.now())
    user_data["answers"] = [] # resetting when test retaken, can fix later
    return jsonify({"status": "started"})


# ----------------------
# FORMATIONS (LEARNING)
# ----------------------
@app.route("/formations/<formation>")
def formations(formation):
    return render_template("formations.html", formation=formation)


# Track when user visits a formation
@app.route("/track_formation", methods=["POST"])
def track_formation():
    formation = request.json.get("formation")
    user_data["formations_visited"].append({
        "formation": formation,
        "time": str(datetime.now())
    })
    return jsonify({"status": "tracked"})


# ----------------------
# QUIZ
# ----------------------

@app.route("/quiz")
def quiz_home():
    if user_data["answers"]:
        answered_ids = {str(a["question_id"]) for a in user_data["answers"]}
        with open("static/data/quiz.json") as f:
            quiz_data = json.load(f)
        total_questions = len(quiz_data)
        for i in range(1, total_questions + 1):
            if str(i) not in answered_ids:
                return redirect(f"/quiz/{i}")
        return redirect("/results")
    return render_template("quiz.html")

@app.route("/quiz/<int:question_id>")
def quiz(question_id):
    with open("static/data/quiz.json") as f:
        quiz_data = json.load(f)

    total_questions = len(quiz_data)

    # If landing on question 1, redirect to first unanswered question
    if question_id == 1:
        answered_ids = {str(a["question_id"]) for a in user_data["answers"]}
        for i in range(1, total_questions + 1):
            if str(i) not in answered_ids:
                question_id = i
                break
        else:
            return redirect("/results")

    question = quiz_data.get(str(question_id))
    if not question:
        return redirect("/results")

    already_answered = any(
        str(a["question_id"]) == str(question_id) for a in user_data["answers"]
    )
    saved_answer = None
    if already_answered:
        saved_answer = next(
            a for a in user_data["answers"] if str(a["question_id"]) == str(question_id)
        )

    return render_template(
        "quiz-questions.html",
        question=question,
        question_id=question_id,
        last=(question_id == total_questions),
        already_answered=already_answered,
        saved_answer=saved_answer,
        review_formation=question_to_formation.get(str(question_id), "433")
    )


# Save quiz answer
@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    question_id = data.get("question_id")
    answer = data.get("answer")

    # load quiz data
    with open("static/data/quiz.json") as f:
        quiz_data = json.load(f)
    
    question = quiz_data[str(question_id)]
    correct = question["correct"]
    explanation = question["explanation"]

    is_correct = (answer == correct)
    user_data["answers"].append({
        "question_id": question_id,
        "answer": answer,
        "correct": is_correct 
        })
    
    review_formation = question_to_formation.get(str(question_id), "433")
    
    return jsonify({
        "correct": is_correct,
        "explanation": explanation,
        "review_url": f"/formations/{review_formation}",
        "status": "saved"
    })

# ----------------------
# RESULTS
# ----------------------
@app.route("/results")
def results():
    with open("static/data/quiz.json") as f:
        quiz_data = json.load(f)
    
    total = len(quiz_data)
    correct = sum(1 for a in user_data["answers"] if a["correct"])

    return render_template("results.html", score=correct, total=total)


# ----------------------
# RUN APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)