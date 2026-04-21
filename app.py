from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simple "database" (since you only need 1 user)
user_data = {
    "start_time": None,
    "formations_visited": [],
    "answers": []
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
@app.route("/quiz/<int:question_id>")
def quiz(question_id):
    return render_template("quiz.html", question_id=question_id)


# Save quiz answer
@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    answer = request.json.get("answer")
    user_data["answers"].append(answer)
    return jsonify({"status": "saved"})


# ----------------------
# RESULTS
# ----------------------
@app.route("/results")
def results():
    # Example correct answers (you can move this to JSON later)
    correct_answers = [1, 0, 1, 1, 0]

    score = 0
    for i in range(min(len(user_data["answers"]), len(correct_answers))):
        if user_data["answers"][i] == correct_answers[i]:
            score += 1

    return render_template("results.html", score=score)


# ----------------------
# RUN APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)