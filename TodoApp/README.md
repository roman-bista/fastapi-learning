database.py
→ creates DB connection

models.py
→ defines tables

main.py
→ starts FastAPI app and defines routes

Concept Purpose

engine------------> manages DB connectivity
Base--------------> parent class for ORM models
models------------> define tables
create_all()------> create tables
Session ---------> active DB conversation
SessionLocal------> creates DB sessions
Column------------> define fields

database.py → DB infrastructure
models.py → table structure
main.py → API logic/routes
todos.db → actual stored data


# JWT Authentication Flow in FastAPI

## What is JWT?

JWT (JSON Web Token) is used for authentication.

After a user logs in successfully, the server generates a token and sends it to the client.

The client stores the token and sends it with future requests.

------------------------------------------------------------------------------------------

# Complete JWT Flow

```text
Login
  ↓
Verify Username & Password
  ↓
Create JWT
  ↓
Return Token
  ↓
Frontend Stores Token
  ↓
Frontend Sends Token
  ↓
get_current_user()
  ↓
Decode JWT
  ↓
Get User
  ↓
Access Protected Route
```

---

# Step 1: User Login

Frontend sends:

```http
POST /token
```

Request:

```json
{
  "username": "roman",
  "password": "password123"
}
```

---

# Step 2: Authenticate User

```python
user = authenticate_user(
    username,
    password,
    db
)
```

Checks:

* User exists
* Password matches bcrypt hash

If invalid:

```python
raise HTTPException(
    status_code=401,
    detail="Invalid username or password"
)
```

---

# Step 3: Create JWT

```python
token = create_access_token(
    user.username,
    user.id,
    timedelta(minutes=20)
)
```

Payload:

```json
{
  "sub": "roman",
  "id": 1,
  "exp": "expiration time"
}
```

JWT Structure:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example:

```text
eyJhbGciOiJIUzI1NiIs...
```

---

# Step 4: Return Token

Backend returns:

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

# Step 5: Frontend Stores Token

Example:

```javascript
localStorage.setItem("token", token)
```

---

# Step 6: Frontend Sends Token

Every protected request:

```http
GET /todos
Authorization: Bearer eyJhbGc...
```

---

# Step 7: Extract Token

```python
oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="token"
)
```

Protected route:

```python
token: str = Depends(oauth2_bearer)
```

FastAPI automatically extracts:

```text
eyJhbGc...
```

from:

```http
Authorization: Bearer eyJhbGc...
```

---

# Step 8: Decode JWT

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

Extract:

```python
username = payload.get("sub")
user_id = payload.get("id")
```

---

# Step 9: Get Current User

```python
async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
):
```

Decode token and return:

```python
{
    "username": username,
    "user_id": user_id
}
```

or fetch user from database.

---

# Step 10: Protected Routes

```python
@router.get("/todos")
async def get_todos(
    current_user = Depends(get_current_user)
):
    return {"message": "Protected Route"}
```

Only authenticated users can access.

---

# Important Components

## SECRET_KEY

Used to sign JWTs.

Generate:

```bash
openssl rand -hex 32
```

Example:

```python
SECRET_KEY = "random_secret_key"
```

---

## ALGORITHM

Usually:

```python
ALGORITHM = "HS256"
```

---

## Expiration Time

```python
expires = datetime.now(timezone.utc) + timedelta(minutes=20)
```

Token becomes invalid after 20 minutes.

---

# FastAPI JWT Packages

Install:

```bash
pip install "python-jose[cryptography]"
pip install passlib[bcrypt]
pip install python-multipart
```

---

# Key Interview Questions

## Authentication vs Authorization

Authentication:

```text
Who are you?
```

Example:

```text
Login
```

Authorization:

```text
What are you allowed to access?
```

Example:

```text
Admin Dashboard
User Dashboard
```

---

# Mental Model

```text
User Login
    ↓
Verify Credentials
    ↓
Create JWT
    ↓
Return JWT
    ↓
Store JWT
    ↓
Send JWT
    ↓
Decode JWT
    ↓
Identify User
    ↓
Allow Access
```

If you understand this flow, you understand the core of JWT Authentication in FastAPI.
