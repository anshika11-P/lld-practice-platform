import os

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# =========================
# PostgreSQL Configuration
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# Problem Table
# =========================

class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)


# =========================
# Practice History
# =========================

class PracticeHistory(db.Model):
    __tablename__ = "practice_history"

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, nullable=False)
    problem_title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    completed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# Home
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# Problems
# =========================

@app.route("/problems")
def problems():

    all_problems = Problem.query.all()

    return render_template(
        "problems.html",
        problems=all_problems
    )


# =========================
# Individual Problem
# =========================

@app.route("/problem/<int:problem_id>")
def problem(problem_id):

    problem_data = Problem.query.get_or_404(problem_id)

    return render_template(
        "problem.html",
        problem=problem_data
    )


# =========================
# Practice Page
# =========================

@app.route("/practice/<int:problem_id>")
def practice(problem_id):

    problem_data = Problem.query.get_or_404(problem_id)

    return render_template(
        "practice.html",
        problem=problem_data
    )


# =========================
# Start Practice
# =========================

@app.route("/start-practice")
def start_practice():

    first_problem = Problem.query.first()

    if first_problem is None:
        return redirect(url_for("problems"))

    return redirect(
        url_for(
            "practice",
            problem_id=first_problem.id
        )
    )


# =========================
# Complete Practice
# =========================

@app.route("/complete/<int:problem_id>", methods=["POST"])
def complete_problem(problem_id):

    problem_data = Problem.query.get_or_404(problem_id)

    history = PracticeHistory(
        problem_id=problem_data.id,
        problem_title=problem_data.title,
        status="Completed"
    )

    db.session.add(history)
    db.session.commit()

    return redirect(url_for("history"))


# =========================
# History
# =========================

@app.route("/history")
def history():

    histories = PracticeHistory.query.order_by(
        PracticeHistory.completed_at.desc()
    ).all()

    return render_template(
        "history.html",
        histories=histories
    )


# =========================
# Learning
# =========================

@app.route("/learning")
def learning():

    return render_template("learning.html")


# =========================
# Feedback
# =========================

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":

        message = request.form.get("message")

        print("Feedback received:", message)

        return redirect(url_for("home"))

    return render_template("feedback.html")


# =========================
# Database Setup
# =========================

def setup_database():

    db.create_all()

    if Problem.query.count() == 0:

        problems = [

            Problem(
                title="Design a Parking Lot",
                description=(
                    "Design a parking lot system where "
                    "different types of vehicles can enter, "
                    "park and exit."
                ),
                difficulty="Easy",
                category="System Design"
            ),

            Problem(
                title="Design a Library Management System",
                description=(
                    "Design a library system to manage books, "
                    "members and borrowing."
                ),
                difficulty="Easy",
                category="Management System"
            ),

            Problem(
                title="Design an Online Food Delivery System",
                description=(
                    "Design a food delivery system with "
                    "restaurants, customers, orders and delivery partners."
                ),
                difficulty="Medium",
                category="Real World"
            ),

            Problem(
                title="Design a Tic Tac Toe Game",
                description=(
                    "Design a two-player Tic Tac Toe game "
                    "using object-oriented programming."
                ),
                difficulty="Medium",
                category="Game"
            ),

            Problem(
                title="Design a Ride Sharing System",
                description=(
                    "Design a ride sharing system with "
                    "riders, drivers and trips."
                ),
                difficulty="Hard",
                category="Real World"
            )
        ]

        db.session.add_all(problems)
        db.session.commit()


# =========================
# Run Application
# =========================

if __name__ == "__main__":

    with app.app_context():
        setup_database()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )