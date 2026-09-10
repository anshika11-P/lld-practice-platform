# LLD Practice Platform

A focused practice platform for learners to practice Low-Level Design (LLD)
problems and receive explainable feedback on their designs.

## Project Goal

The platform follows this learning journey:

Choose Problem → Think & Design → Submit → Get Feedback → Review → History

The main focus is on:

- Classes and interfaces
- Responsibilities
- Relationships between classes
- Abstraction
- Extensibility
- Design decisions

## Features

- Multiple LLD practice problems
- Problem details and difficulty levels
- Guided LLD practice
- Solution submission
- Deterministic design evaluation
- Explainable feedback
- Scores for important LLD concepts
- Strengths and improvement suggestions
- Recommended next steps
- Practice history
- Learning guide
- PostgreSQL database
- Automated tests

## Tech Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy

### Frontend

- HTML
- CSS
- Jinja Templates

### Database

- PostgreSQL

### Testing

- Pytest

## Project Structure

```text
LLD Practice Platform/
│
├── app.py
├── test_app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── problems.html
│   ├── problem.html
│   ├── practice.html
│   ├── feedback.html
│   ├── history.html
│   └── learning.html
│
└── static/
    └── style.css