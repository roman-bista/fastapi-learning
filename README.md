---

## 📚 What I'm Learning

### ✅ Completed
- FastAPI setup and project structure
- GET, POST, PUT, DELETE request methods
- Path Parameters & Query Parameters
- Pydantic Models & Request Validation
- HTTP Status Codes
- Swagger / OpenAPI Documentation

### 🔄 In Progress
- SQLAlchemy ORM
- PostgreSQL Database Integration
- User Authentication & Authorization
- Password Hashing (bcrypt)
- JWT Authentication

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| FastAPI | API Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| JWT | Authentication |
| Pydantic | Data Validation |

---

## 🔜 Roadmap

- [x] FastAPI Basics & CRUD
- [ ] Todo App with Database
- [ ] JWT Authentication System
- [ ] Full Backend Project

---

## 📌 How to Run

```bash
# Clone the repo
git clone https://github.com/roman-bista/FastApi_Learning.git

# Go to project folder
cd FastApi_Learning

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2

# Run any project
uvicorn main:app --reload
```

---

> 🧠 Learning backend engineering step by step — built with curiosity and consistency.

User Login
    ↓
Username + Password
    ↓
Verify password
    ↓
create_access_token()
    ↓
JWT Token
    ↓
Client stores token
------------------------------------------------
GET /todos
Authorization: Bearer eyJhbGc...
    ↓
OAuth2PasswordBearer
    ↓
token = "eyJhbGc..."
    ↓
get_current_user()
    ↓
jwt.decode()
    ↓
payload
    ↓
sub + id
    ↓
current_user
    ↓
/todos route


<<-------------------------------------------->><<-------------------------------------------->>
<<-------------------------------------------->><<-------------------------------------------->>



USER REGISTRATION
=================

POST /auth/
    ↓
Receive username, password, email
    ↓
Hash password using bcrypt
    ↓
Store Worker in database
    ↓
User created


--------------------------------------------------


USER LOGIN
==========

POST /auth/token
    ↓
Receive username + password
    ↓
Find Worker in database
    ↓
Verify password using bcrypt
    ↓
If invalid
    ↓
401 Unauthorized

If valid
    ↓
create_access_token()
    ↓
Calculate expiration time
    ↓
Create payload

{
    "sub": username,
    "id": user_id,
    "exp": expires
}

    ↓
jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
)

    ↓
JWT Token Generated

eyJhbGciOiJIUzI1NiIs...

    ↓
Return

{
    "access_token": "...",
    "token_type": "bearer"
}

    ↓
Client stores JWT


--------------------------------------------------


PROTECTED REQUEST
=================

GET /todos
Authorization: Bearer eyJhbGc...

    ↓
Request arrives

    ↓
OAuth2PasswordBearer

Authorization: Bearer eyJhbGc...
                ↓
Extract token
                ↓

token = "eyJhbGc..."

    ↓
Pass token to

get_current_user(token)

    ↓
jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)

    ↓
Verify Signature

Is SECRET_KEY valid?
    ↓
Yes / No

    ↓
Check Expiration

exp > current_time ?
    ↓
Yes / No

    ↓
Decode Payload

{
    "sub": "roman",
    "id": 1,
    "exp": ...
}

    ↓
Extract Values

username = payload.get("sub")
user_id = payload.get("id")

    ↓
Check

username is None?
user_id is None?

    ↓
If invalid
401 Unauthorized

    ↓
If valid

return {
    "username": username,
    "user_id": user_id
}

    ↓
current_user


--------------------------------------------------


AUTHORIZATION
=============

Route receives:

current_user = Depends(
    get_current_user
)

    ↓

{
    "username": "roman",
    "user_id": 1
}

    ↓

Filter todos

db.query(Todos).filter(
    Todos.owner_id ==
    current_user["user_id"]
)

    ↓

Roman only sees Roman's todos


--------------------------------------------------


COMPLETE JWT FLOW
=================

Login
    ↓
Verify Credentials
    ↓
Create JWT
    ↓
Return JWT
    ↓
Client Stores JWT
    ↓
Client Sends JWT
    ↓
OAuth2PasswordBearer Extracts JWT
    ↓
get_current_user()
    ↓
Verify SECRET_KEY Signature
    ↓
Check Expiration
    ↓
Decode Payload
    ↓
Get Username + User ID
    ↓
Identify Current User
    ↓
Authorize Request
    ↓
Allow Access