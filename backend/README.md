# Backend Side

## Installation Guide (Python 3.11)

Set up the project on **macOS, Linux, or Windows** using Python 3.11.

- All commands shown needs to be executed from the `backend` folder.

---

### Check Python 3.11 Installation

Verify your Python version:

```sh
python --version
```

If Python 3.11 is not installed, download it from the [official Python website](https://www.python.org/downloads/).

---

### Create & Activate a Virtual Environment

**macOS & Linux:**

```sh
python -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**

```bat
python -m venv venv
venv\Scripts\activate
```

---

### Install Dependencies

With the virtual environment activated, run:

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Migrate the Alembic migrations

To create the **SQLite** DB and migrate the models execute the following command:

```sh
alembic upgrade head
```

With this action `database.db` file will be generated.

### Run the Project

Start the **Fast API** server:

```sh
python -m app.main
```

The API will execute in the following URL `http://117.0.0.1:8000`.

#### Swagger Documentation

You can find the Swagger Documentation after running the API server at:

```sh
http://localhost:8000/docs
```
