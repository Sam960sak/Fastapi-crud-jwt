# Expense Tracker API

A FastAPI REST API with user registration, login, JWT authentication and a full
CRUD resource (**expenses**) where every record belongs to the logged-in user.

## Concept

An expense tracker. Each expense has 6 fields: `title`, `description`, `amount`,
`category`, `status` and `created_at`. Every user only sees and manages their
own expenses.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then set your own SECRET_KEY
uvicorn app.main:app --reload
```

Open Swagger at http://127.0.0.1:8000/docs

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Secret used to sign JWTs (required) | — |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `30` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./expense_tracker.db` |

`.env.example` is committed, the real `.env` is not.

## Endpoints

| Method | Route | Auth | Purpose | Success |
|---|---|---|---|---|
| POST | `/auth/register` | No | Create a user (bcrypt hashed password) | 201 / 409 |
| POST | `/auth/login` | No | Get a JWT access token | 200 / 401 |
| GET | `/auth/me` | Yes | Current user | 200 / 401 |
| POST | `/expenses` | Yes | Create an expense | 201 / 422 |
| GET | `/expenses?skip=0&limit=10` | Yes | List my expenses (paginated) | 200 / 401 |
| GET | `/expenses/{id}` | Yes | Get one expense | 200 / 404 |
| PUT | `/expenses/{id}` | Yes | Update an expense | 200 / 404 / 422 |
| DELETE | `/expenses/{id}` | Yes | Delete an expense | 204 / 404 |

Requests other than register/login need the header:
`Authorization: Bearer <access_token>`

## Project structure

```
app/
  main.py            # FastAPI app + router registration
  config.py          # settings loaded from .env
  database.py        # engine, session, Base
  models.py          # SQLAlchemy models (User, Expense)
  schemas.py         # Pydantic request/response models
  auth.py            # password hashing, JWT create/validate, current-user dependency
  routers/
    auth.py          # /auth routes
    expenses.py      # /expenses CRUD routes
```
