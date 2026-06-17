# TEST_LEARNING.md

# FastAPI Testing Notes

╔════════════════════════════════╗
║              ║
╚════════════════════════════════╝
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PYTEST FIXTURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
---

# Why Testing?

Testing verifies that our code behaves as expected.

Benefits:

* Prevent bugs
* Catch regressions
* Verify API responses
* Make refactoring safer
* Improve code confidence

---

# Pytest

Pytest is the most popular Python testing framework.

Install:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

---

# Test Naming Rules

Pytest automatically discovers:

Files:

```text
test_*.py
*_test.py
```

Examples:

```text
test_main.py
test_todos.py
```

Functions:

```python
def test_something():
```

Must start with:

```python
test_
```

---

# Assert

Assertions verify expected behavior.

Example:

```python
assert 2 + 2 == 4
```

Passes because:

```python
4 == 4
```

Example:

```python
assert 2 + 2 == 5
```

Fails because:

```python
4 != 5
```

Mental Model:

```text
assert condition

If True  → PASS
If False → FAIL
```

Equivalent to:

```python
if not condition:
    raise AssertionError
```

---

# Testing Classes

Example:

```python
class Student:
    def __init__(
        self,
        first_name,
        last_name,
        major,
        years
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
```

Test:

```python
def test_person_initialization():
    student = Student(
        "john",
        "doe",
        "cs",
        3
    )

    assert student.first_name == "john"
    assert student.last_name == "doe"
    assert student.major == "cs"
    assert student.years == 3
```

Purpose:

Verify constructor stores values correctly.

---

# Fixtures

Fixtures provide reusable setup data.

Without Fixture:

```python
student = Student(...)
```

Repeated in every test.

With Fixture:

```python
@pytest.fixture
def default_student():
    return Student(
        "john",
        "doe",
        "cs",
        3
    )
```

Use:

```python
def test_student(default_student):
    assert default_student.first_name == "john"
```

Pytest automatically injects the fixture.

Mental Model:

```text
Test
 ↓
Needs Fixture
 ↓
Run Fixture
 ↓
Provide Object
 ↓
Run Test
```

---

# FastAPI Testing

FastAPI provides:

```python
from fastapi.testclient import TestClient
```

Purpose:

Send fake HTTP requests without running a real browser.

Example:

```python
client = TestClient(app)
```

Available Methods:

```python
client.get()
client.post()
client.put()
client.delete()
```

---

# Health Check Endpoint

Route:

```python
@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
```

Test:

```python
def test_return_health_check():
    response = client.get("/healthy")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Healthy"
    }
```

---

# How TestClient Works

Visual Flow:

```text
pytest
    ↓
TestClient
    ↓
FastAPI App
    ↓
Route Function
    ↓
Response
    ↓
Assertions
```

Example:

```text
client.get("/healthy")
        ↓
health_check()
        ↓
{"status":"Healthy"}
        ↓
assertions
        ↓
PASS
```

---

# Response Object

Status Code:

```python
response.status_code
```

Example:

```python
assert response.status_code == 200
```

Checks request success.

JSON Response:

```python
response.json()
```

Example:

```python
assert response.json() == {
    "status": "Healthy"
}
```

Checks response body.

---

# Package Imports

Project Structure:

```text
FastApi/
└── TodoApp/
    ├── main.py
    ├── routers/
    └── test/
```

Run Application:

```bash
uvicorn TodoApp.main:app --reload
```

Test Import:

```python
from TodoApp.main import app
```

Reason:

TodoApp is treated as a Python package.

---

# Common Errors

## No module named 'main'

Error:

```text
ModuleNotFoundError:
No module named 'main'
```

Fix:

```python
from TodoApp.main import app
```

Run pytest from parent folder:

```bash
cd FastApi
pytest
```

---

## Relative Import Error

Error:

```text
attempted relative import with no known parent package
```

Cause:

Using:

```python
from .routers import auth
```

while running:

```bash
uvicorn main:app
```

Fix:

Run as package:

```bash
uvicorn TodoApp.main:app --reload
```

---

# Database Testing

Purpose:

Never test against the real PostgreSQL database.

Create a separate test database.

Example:

```python
SQLALCHEMY_DATABASE_URL =
"sqlite:///./testdb.db"
```

---

# Testing Database Flow

Normal Application:

```text
Request
    ↓
get_db()
    ↓
SessionLocal()
    ↓
PostgreSQL
```

Testing:

```text
Request
    ↓
override_get_db()
    ↓
TestingSessionLocal()
    ↓
SQLite Test Database
```

---

# Test Session

Create:

```python
TestingSessionLocal =
sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

Purpose:

Provide database sessions for testing.

---

# Create Tables for Testing

```python
Base.metadata.create_all(
    bind=engine
)
```

Creates all tables in:

```text
testdb.db
```

---

# Current Testing Skills

Completed:

✅ Pytest Basics

✅ Assertions

✅ Test Discovery

✅ Fixtures

✅ FastAPI TestClient

✅ Health Check Testing

✅ Package Imports

✅ Test Database Setup

Learning Next:

⬜ CRUD Route Testing

⬜ Authentication Testing

⬜ Dependency Overrides

⬜ Mocking

⬜ Database Assertions

⬜ Integration Testing


Visual Flow::

Normal App:

Request
   ↓
get_db()
   ↓
SessionLocal()
   ↓
PostgreSQL

Testing:

Request
   ↓
override_get_db()
   ↓
TestingSessionLocal()
   ↓
SQLite testdb.db
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<!-- /////////////////////////////// -->

Create Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

Creates:

testdb.db

A completely separate database.

Create Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

Connects SQLAlchemy to:

testdb.db
Create Testing Session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Creates database sessions specifically for tests.

Create Tables
Base.metadata.create_all(bind=engine)

Creates:

users table
todos table

inside:

testdb.db
Override Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

This function will replace:

get_db()

during tests

FastAPI Dependency Injection

Production:
get_db()
   ↓
PostgreSQL


Testing:
get_db()
   ↓
OVERRIDDEN
   ↓
override_get_db()
   ↓
SQLite Test DB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- /////////////////////////////////////// -->

╔════════════════════════════════╗
║  response.json()  
╚════════════════════════════════╝
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PYTEST - response.json()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

response = client.get("/todos/1")

response.json()
→ Returns API response data (JSON) as a Python dict/list.

Flow:
Request
  ↓
API Route
  ↓
JSON Response
  ↓
response.json()
  ↓
Python dict/list

Examples:

print(response.json())

assert response.json()["title"] == "Learn FastAPI"
assert response.json() == expected_data
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 get_db() & override_get_db()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Definition:
- get_db() creates a database session and provides it to FastAPI routes.
- override_get_db() replaces get_db() during testing to use testdb.db.

Key Points:
- Creates a DB session using SessionLocal().
- Allows CRUD operations inside routes.
- Uses yield to provide the session.
- Automatically closes the session after the request.
- override_get_db() makes tests use SQLite testdb.db instead of PostgreSQL.

Example:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Flow:
Request
   ↓
get_db()
   ↓
DB Session (db)
   ↓
CRUD Operations
   ↓
db.close()

Remember:
- get_db() = Open DB session → Use DB → Close DB session.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Password Hashing (bcrypt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Definition:
- Converts a plain password into a secure hashed string before storing it in the database.

Key Points:
- Never store plain passwords.
- bcrypt adds a random salt automatically.
- Same password produces different hashes.
- Use verify() during login.

Example:
hashed_password = bcrypt_context.hash("roman")

bcrypt_context.verify(
    "roman",
    hashed_password
)  # True

Flow:
Password
   ↓
bcrypt.hash()
   ↓
Hashed Password
   ↓
Store in DB

Remember:
- Hash passwords, never store them as plain text.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def      → normal function
async def → async function

Call normal:
result = func()

Call async:
result = await func()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Health Check Route
✓ Todo Model
✓ Read Todos
✓ Read Todo By ID
✓ Todo Not Found
✓ Create Todo
✓ Update Todo
✓ Update Todo Not Found
✓ Delete Todo
✓ Delete Todo Not Found

✓ Admin Read Todos
✓ Admin Delete Todo
✓ Admin Delete Todo Not Found

✓ Get User
✓ Change Password
✓ Change Password Invalid
✓ Change Phone Number

✓ authenticate_user()
✓ authenticate_user() wrong username
✓ authenticate_user() wrong password

✓ create_access_token()
✓ get_current_user()
✓ get_current_user() invalid payload


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
