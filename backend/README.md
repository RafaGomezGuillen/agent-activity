# Backend

The backend is a FastAPI service for Agent Activity. It registers agents, stores metrics and activity data, serves screenshots, manages commands, and runs scheduled maintenance jobs.

![Backend docs - Swagger UI](../assets/backend/docs.png)

## Stack

- Python 3.11 or or higher.
- FastAPI and Uvicorn.
- SQLAlchemy.
- Alembic.
- SQLite.
- APScheduler.
- Pydantic 2.

## Setup

Run all commands from `backend/`.

```sh
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
python -m app.main
```

On Windows:

```bat
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
python -m app.main
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## Database

The SQLite URL is configured in `app/db/database.py`:

```text
sqlite:///./database.db
```

After `alembic upgrade head`, the database file is created as:

```text
backend/database.db
```

Migration files live in `alembic/versions/`.

Common Alembic commands:

```sh
alembic upgrade head
alembic revision --autogenerate -m "describe change"
alembic downgrade -1
```