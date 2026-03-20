# Agent Side

## Installation Guide (Python 3.11)

Set up the project on **macOS, Linux, or Windows** using Python 3.11. 

* All commands shown needs to be executed from the `agent` folder.

---

### Check Python 3.11 Installation

Verify your Python version:

```sh
python3 --version
```

If Python 3.11 is not installed, download it from the [official Python website](https://www.python.org/downloads/).

---

### Create & Activate a Virtual Environment

**macOS & Linux:**

```sh
python3.11 -m venv venv
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

### Run the Project

Start the **Agent**:

```sh
python main.py
```
