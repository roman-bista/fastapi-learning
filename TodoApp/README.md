# TodoApp API

A production-style Todo Management API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT Authentication, and Pytest.

## Features

### Authentication

* User Registration
* User Login
* JWT Token Authentication
* Password Hashing with Passlib
* Protected Routes

### Todo Management

* Create Todo
* Read Todos
* Update Todo
* Delete Todo
* User-specific Todos

### Administration

* Admin Routes
* Role-based Authorization

### Database

* PostgreSQL Database
* SQLAlchemy ORM
* Alembic Database Migrations

### Testing

* Pytest
* FastAPI TestClient
* Health Check Endpoint Testing
* Test Database Configuration

---

## Tech Stack

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Passlib
* JWT Authentication
* Pytest
* Uvicorn

---

## Project Structure

```text
TodoApp/
│
├── alembic/
│   └── versions/
│
├── routers/
│   ├── auth.py
│   ├── todos.py
│   ├── admin.py
│   └── users.py
│
├── test/
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_todos.py
│   └── test_example.py
│
├── main.py
├── database.py
├── models.py
├── alembic.ini
├── pytest.ini
├── README.md
└── LEARNING.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd TodoApp
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Create PostgreSQL database:

```sql
CREATE DATABASE TodoApplicationDatabase;
```

Configure your database connection in:

```python
database.py
```

Example:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/TodoApplicationDatabase"
```

---

## Alembic Migrations

Generate migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migration:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

---

## Running the Application

From the parent directory:

```bash
uvicorn TodoApp.main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Health Check Endpoint

Endpoint:

```http
GET /healthy
```

Response:

```json
{
    "status": "Healthy"
}
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Current tests include:

* Pytest Basics
* Health Check Endpoint Testing
* FastAPI TestClient Testing
* Test Database Configuration

---

## Learning Objectives

This project is part of my Backend Engineering learning journey.

Topics covered:

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT Authentication
* API Development
* Database Design
* Testing with Pytest

Upcoming Topics:

* CRUD Route Testing
* Authentication Testing
* Database Testing
* Docker
* Deployment
* CI/CD
* System Design

---

## Author

Roman Bista

Backend Engineering Learning Journey

Nepal 🇳🇵
