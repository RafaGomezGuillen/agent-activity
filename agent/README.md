# Agent

![Agent logs](../assets/agent/agent.png)

The agent is a Python endpoint process for Agent Activity. It registers the host with the backend, sends periodic system metrics, polls for commands, and on supported desktop platforms starts background services for keylogging, clipboard monitoring, and screenshots.

> [!CAUTION]
> Use it only on machines where this monitoring is authorized and disclosed.

## Stack

- Python 3.11 or higher.
- `psutil` for system metrics and process data.
- `requests` for backend communication.
- `pynput`, `pyperclip`, `Pillow`, and `pyscreenshot` for activity capture on supported platforms.
- `rumps` and `pyobjc` for the macOS menu bar bundle.
- `pystray` and `pywin32` for the Windows tray app.
- PyInstaller for packaged executables.

## Setup

Run all commands from `agent/`.

```sh
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Windows:

```bat
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Linux:

```sh
sudo apt install python3.10-venv binutils -y
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Configuration lives in `config/settings.py`.

Important values:

- `SERVER_URL`: backend API URL. Defaults to `http://localhost:8000`.
- `METRICS_INTERVAL`: seconds between heartbeat metrics and command polling.
- `APP_NAME`: packaged app/service name, currently `agent-activity`.
- `DATA_DIR`: local relative data directory for source runs.
- `LOGS_DIR`: local relative logs directory for source runs.
- `KEYLOG_SEND_INTERVAL`, `CLIPBOARD_SEND_INTERVAL`, `SCREENSHOT_INTERVAL`: activity upload intervals.
- `MAX_FILE_SIZE`: maximum file size accepted by the `filesystem.read_file` command.

## Run From Source

Start the backend first, then run:

```sh
python main.py
```

- On Windows and macOS, background services are started from the loop for keylogs, clipboard events, and screenshots. 
- On Linux, the current agent loop only sends metrics and polls commands unless platform-specific capture behavior is extended.

## Local Data

When running from source, the agent writes relative to `agent/`:

- `data/agent_id.txt`
- `data/keylog.jsonl`
- `data/clipboard.jsonl`
- `data/screenshots/`
- `logs/`

Packaged builds redirect data and logs to OS-specific application data folders. See the platform README files under `pkgs/`.

## Packaging

- [Linux packaging](pkgs/linux/README.md)
- [macOS packaging](pkgs/mac/README.md)
- [Windows packaging](pkgs/windows/README.md)

Shared PyInstaller settings live in `pkgs/pyinstaller_config.py`.
