from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:1234@localhost:5432/lld_practice"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# Problem Model
# =========================

class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)


# =========================
# Practice History Model
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
# Submission Model
# =========================

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, nullable=False)
    problem_title = db.Column(db.String(200), nullable=False)

    solution = db.Column(
        db.Text,
        nullable=False
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# Feedback Model
# =========================

class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    submission_id = db.Column(
        db.Integer,
        nullable=False
    )

    responsibility_score = db.Column(
        db.Integer,
        nullable=False
    )

    abstraction_score = db.Column(
        db.Integer,
        nullable=False
    )

    relationship_score = db.Column(
        db.Integer,
        nullable=False
    )

    extensibility_score = db.Column(
        db.Integer,
        nullable=False
    )

    strengths = db.Column(
        db.Text,
        nullable=False
    )

    improvements = db.Column(
        db.Text,
        nullable=False
    )

    next_steps = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
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
# Problem Details
# =========================

@app.route("/problem/<int:problem_id>")
def problem(problem_id):

    problem_data = Problem.query.get_or_404(
        problem_id
    )

    return render_template(
        "problem.html",
        problem=problem_data
    )


# =========================
# Practice
# =========================

@app.route("/practice/<int:problem_id>")
def practice(problem_id):

    problem_data = Problem.query.get_or_404(
        problem_id
    )

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
        return redirect(
            url_for("problems")
        )

    return redirect(
        url_for(
            "practice",
            problem_id=first_problem.id
        )
    )


# =========================
# Submit Solution
# =========================

@app.route(
    "/submit/<int:problem_id>",
    methods=["POST"]
)
def submit_solution(problem_id):

    problem_data = Problem.query.get_or_404(
        problem_id
    )

    solution = request.form.get(
        "solution",
        ""
    ).strip()

    if not solution:

        return render_template(
            "practice.html",
            problem=problem_data,
            error="Please write your solution before submitting."
        )

    submission = Submission(

        problem_id=problem_data.id,

        problem_title=problem_data.title,

        solution=solution
    )

    db.session.add(submission)

    db.session.commit()

    return redirect(
        url_for(
            "evaluate_submission",
            submission_id=submission.id
        )
    )


# =========================
# Evaluate Submission
# =========================

@app.route(
    "/evaluate/<int:submission_id>"
)
def evaluate_submission(submission_id):

    submission = Submission.query.get_or_404(
        submission_id
    )

    solution = submission.solution.lower()

    # -------------------------
    # Basic deterministic checks
    # -------------------------

    responsibility_score = 1
    abstraction_score = 1
    relationship_score = 1
    extensibility_score = 1

    # Responsibility check
    if (
        "responsibility" in solution
        or "responsibilities" in solution
        or "method" in solution
    ):
        responsibility_score = 4

    elif "class" in solution:
        responsibility_score = 3

    # Abstraction check
    if (
        "interface" in solution
        or "abstract" in solution
    ):
        abstraction_score = 5

    elif "class" in solution:
        abstraction_score = 3

    # Relationship check
    if (
        "relationship" in solution
        or "composition" in solution
        or "association" in solution
        or "inheritance" in solution
    ):
        relationship_score = 5

    elif "class" in solution:
        relationship_score = 3

    # Extensibility check
    if (
        "strategy" in solution
        or "interface" in solution
        or "extensible" in solution
        or "extension" in solution
    ):
        extensibility_score = 5

    elif "class" in solution:
        extensibility_score = 3

    # -------------------------
    # Feedback generation
    # -------------------------

    strengths = []

    improvements = []

    next_steps = []

    if responsibility_score >= 4:

        strengths.append(
            "You have considered responsibilities and methods."
        )

    else:

        improvements.append(
            "Clearly define the responsibility of each class."
        )

        next_steps.append(
            "Write one main responsibility for every class."
        )

    if abstraction_score >= 4:

        strengths.append(
            "Your design shows awareness of abstraction."
        )

    else:

        improvements.append(
            "Consider interfaces or abstractions where behavior may vary."
        )

        next_steps.append(
            "Identify behavior that could be represented using an interface."
        )

    if relationship_score >= 4:

        strengths.append(
            "You have considered relationships between classes."
        )

    else:

        improvements.append(
            "Explain how your classes interact with each other."
        )

        next_steps.append(
            "Draw or describe the relationships between your main classes."
        )

    if extensibility_score >= 4:

        strengths.append(
            "Your design considers future changes."
        )

    else:

        improvements.append(
            "Think about how the design can support new requirements."
        )

        next_steps.append(
            "Identify one part of the system that may change in the future."
        )

    if not strengths:

        strengths.append(
            "You attempted the problem and identified a starting structure."
        )

    if not improvements:

        improvements.append(
            "The design is reasonably structured. Look for edge cases and future requirements."
        )

    if not next_steps:

        next_steps.append(
            "Try improving the design by considering alternative implementations."
        )

    feedback = Feedback(

        submission_id=submission.id,

        responsibility_score=responsibility_score,

        abstraction_score=abstraction_score,

        relationship_score=relationship_score,

        extensibility_score=extensibility_score,

        strengths="\n".join(
            "• " + item
            for item in strengths
        ),

        improvements="\n".join(
            "• " + item
            for item in improvements
        ),

        next_steps="\n".join(
            "• " + item
            for item in next_steps
        )
    )

    db.session.add(feedback)

    # Add completion history
    history = PracticeHistory(

        problem_id=submission.problem_id,

        problem_title=submission.problem_title,

        status="Submitted & Evaluated"
    )

    db.session.add(history)

    db.session.commit()

    return redirect(
        url_for(
            "feedback_result",
            submission_id=submission.id
        )
    )


# =========================
# Feedback Result
# =========================

@app.route(
    "/feedback-result/<int:submission_id>"
)
def feedback_result(submission_id):

    submission = Submission.query.get_or_404(
        submission_id
    )

    feedback = Feedback.query.filter_by(
        submission_id=submission_id
    ).first()

    return render_template(
        "feedback.html",
        submission=submission,
        feedback=feedback
    )


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

    return render_template(
        "learning.html"
    )


# =========================
# Feedback Page
# =========================

@app.route(
    "/feedback",
    methods=["GET", "POST"]
)
def feedback():

    if request.method == "POST":

        message = request.form.get(
            "message"
        )

        print(
            "Feedback received:",
            message
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "feedback.html"
    )


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
                    "restaurants, customers, orders and "
                    "delivery partners."
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

        db.session.add_all(
            problems
        )

        db.session.commit()


# =========================
# Run Application
# =========================

if __name__ == "__main__":

    with app.app_context():

        setup_database()

    app.run(debug=True) 