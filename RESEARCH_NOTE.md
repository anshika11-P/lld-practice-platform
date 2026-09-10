# Research Note — LLD Practice Platform

## 1. Problem Understanding

The goal of the LLD Practice Platform is to help learners practice
Low-Level Design problems in a structured way.

A learner should be able to:

1. Choose an LLD problem
2. Understand the requirements
3. Think about the design
4. Submit the design
5. Receive useful feedback
6. Understand what can be improved
7. Review previous attempts

The platform should focus on design thinking rather than only checking
whether a particular answer is correct.

---

## 2. What Should a Learner Provide?

A meaningful LLD attempt should contain enough information to understand
the learner's design decisions.

The learner should provide:

### Classes

The main classes or entities identified for the problem.

### Responsibilities

The responsibility of each class.

### Relationships

How different classes interact with each other.

Examples include:

- Association
- Composition
- Inheritance

### Interfaces and Abstractions

The learner can mention interfaces or abstractions when different
implementations or changing behavior are expected.

### Design Decisions

The learner should explain important choices and how the design could
handle future changes.

This gives the evaluator enough information to provide meaningful
feedback.

---

## 3. What Makes Feedback Useful?

LLD problems can have multiple valid solutions.

Therefore, the platform should not simply compare the learner's answer
with one fixed "correct answer."

Useful feedback should focus on design principles such as:

- Clear responsibilities
- Low coupling
- Appropriate abstraction
- Meaningful relationships
- Extensibility
- Separation of concerns

Feedback should answer three questions:

### What did I do well?

The learner should understand which parts of the design are already good.

### What could be improved?

The learner should receive specific and actionable suggestions.

### What should I do next?

The learner should get a practical next step for improving their design.

---

## 4. Deterministic vs LLM Evaluation

There are two useful evaluation approaches.

### Deterministic Evaluation

Rule-based checks can identify explicit concepts in a submission.

For example:

- Class
- Interface
- Abstract
- Composition
- Association
- Inheritance
- Strategy
- Responsibility
- Extensibility

Advantages:

- Predictable
- Explainable
- Easy to test
- Fast
- No external AI dependency

The current MVP uses this approach.

### LLM Evaluation

An LLM could provide deeper semantic feedback.

For example, it could understand whether a class has too many
responsibilities or whether an abstraction is actually useful.

Advantages:

- Better understanding of natural language
- More detailed feedback
- Can evaluate different valid designs

However, LLM evaluation can be less predictable and may require
additional validation.

### Proposed Future Approach

The platform can support both approaches:

```text
Submission
    |
    v
Evaluation Strategy
    |
    +---- Rule Based Evaluator
    |
    +---- LLM Evaluator
    |
    v
Common Feedback Format