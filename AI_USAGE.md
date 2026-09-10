# AI Usage

AI tools were used during the development of the LLD Practice Platform
for brainstorming, implementation guidance, debugging and documentation.

## 1. Product and Feature Planning

### AI Assistance

AI was used to brainstorm features for the learner journey:

Choose Problem → Think/Design → Submit → Get Feedback → Review → History

### Decision

Accepted.

### Why?

This helped structure the MVP around the actual learner workflow instead
of adding unnecessary features.

---

## 2. Evaluation and Feedback Approach

### AI Assistance

AI was used to compare possible evaluation approaches, including
deterministic rules and LLM-based evaluation.

### Decision

For the MVP, deterministic rule-based evaluation was accepted.

### Why?

It is:

- Simple to implement
- Easy to test
- Explainable to learners
- Predictable
- Suitable for a 2-day assignment

LLM-based evaluation can be added later as another evaluation strategy.

---

## 3. Backend and Database Design

### AI Assistance

AI was used to review the domain entities and suggest separation of:

- Problem
- Submission
- Feedback
- PracticeHistory

### Decision

Accepted with modifications.

### Why?

Separating these entities makes the domain easier to understand and
allows future evaluation approaches to be added without mixing problem,
submission and feedback data.

---

## 4. Debugging and Testing

### AI Assistance

AI was used to identify and fix issues during development, including
Flask route problems, template issues and test failures.

### Decision

Accepted after manually verifying the application.

### Why?

AI suggestions were not blindly accepted. Changes were tested locally
before being considered complete.

The application tests were run using:

```bash
pytest