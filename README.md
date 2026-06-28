# 🚀 FastAPI Todo Application

A production-ready Todo Application built while learning backend development with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **JWT Authentication**, **Pytest**, and **Docker**.

---

# 📌 Features

* User Registration
* User Login
* JWT Authentication
* Password Hashing (bcrypt)
* Create Todo
* Read Todos
* Update Todo
* Delete Todo
* User Authorization
* Admin Routes
* Database Migrations (Alembic)
* Unit Testing (Pytest)
* Dockerized FastAPI Application
* PostgreSQL with Docker Compose

---

# 🛠 Tech Stack

### Backend

* Python 3
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* SQLite (during development)
* Alembic

### Authentication

* JWT
* OAuth2PasswordBearer
* Passlib (bcrypt)

### Testing

* Pytest
* TestClient

### DevOps

* Docker
* Docker Compose
* Docker Hub

---

# 📂 Project Structure

```
FastApi/
│
├── TodoApp/
│   ├── routers/
│   ├── templates/
│   ├── static/
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── ...
│
├── test/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
└── alembic.ini
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/roman-bista/<YOUR_REPOSITORY>.git
cd <YOUR_REPOSITORY>
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
uvicorn TodoApp.main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

---

# 🐳 Running with Docker Compose

Build the application:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

---

# 📦 Docker Images

The application is available as a Docker image on Docker Hub.

Example:

```bash
docker pull roman49/todoapp-docker:latest
```

---

# 🗄 Database

Development:

* SQLite

Docker:

* PostgreSQL 16

ORM:

* SQLAlchemy

Migration Tool:

* Alembic

---

# 🔐 Authentication

The application uses:

* JWT Access Tokens
* OAuth2PasswordBearer
* Password Hashing with bcrypt

---

# 🧪 Testing

Run tests:

```bash
pytest
```

---

# 📖 What I Learned

* Python Backend Development
* FastAPI Fundamentals
* REST API Design
* CRUD Operations
* SQLAlchemy ORM
* PostgreSQL
* Alembic Migrations
* JWT Authentication
* Dependency Injection
* Pytest
* Docker
* Docker Compose
* Docker Networking
* Docker Volumes
* Docker Hub

---

# 🗺 Learning Roadmap

* ✅ Python
* ✅ Git & GitHub
* ✅ FastAPI
* ✅ SQLAlchemy
* ✅ SQLite
* ✅ PostgreSQL
* ✅ Alembic
* ✅ JWT Authentication
* ✅ Testing (Pytest)
* ✅ Docker
* ✅ Docker Compose
* ✅ Docker Hub
* ⏳ Deployment
* ⏳ CI/CD
* ⏳ Redis
* ⏳ Production Architecture
* ⏳ Kubernetes

---

# 👨‍💻 Author

**Roman Bista**

Backend Developer | FastAPI | Python | PostgreSQL | Docker

GitHub: https://github.com/roman-bista
