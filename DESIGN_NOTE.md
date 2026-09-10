# Design Note — LLD Practice Platform

## 1. Architecture

The application follows a simple Flask monolithic architecture.

```text
Browser
   |
   v
Flask Routes
   |
   +------------------+
   |                  |
   v                  v
Templates          Evaluation
   |                  |
   +--------+---------+
            |
            v
        PostgreSQL