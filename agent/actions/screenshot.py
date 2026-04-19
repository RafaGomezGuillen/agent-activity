import os
import platform
import time
import threading
import datetime
import logging
from typing import Optional

from api.client import upload_screenshot
from config.settings import (
    SCREENSHOT_FOLDER,
    SCREENSHOT_MAX_COUNT,
    SCREENSHOT_INTERVAL,
    SCREENSHOT_QUALITY
)

SCREENSHOT_BACKEND = None

try:
    from PIL import Image
    from PIL import ImageGrab as PILImageGrab
except ImportError:
    Image = None
    PILImageGrab = None

try:
    import pyscreenshot
except ImportError:
    pyscreenshot = None

SYSTEM = platform.system()

if SYSTEM in {"Windows", "Darwin"} and PILImageGrab is not None:
    SCREENSHOT_BACKEND = "pillow"
elif pyscreenshot is not None and Image is not None:
    SCREENSHOT_BACKEND = "pyscreenshot"

logger = logging.getLogger("screenshot")
logging.basicConfig(level=logging.INFO)

# =========================
# STATE
# =========================
AGENT_ID = None
STOP_EVENT = threading.Event()
SCREENSHOT_THREAD = None # running thread reference for screenshots

# =========================
# FILE SETUP
# =========================
def _ensure_folder():
    """Ensure the screenshot folder exists."""
    os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

# =========================
# HELPERS
# =========================
def _now_timestamp():
    """Get current timestamp for filename."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def _cleanup_old_screenshots():
    """Remove oldest screenshots if exceeding max count."""
    try:
        files = [f for f in os.listdir(SCREENSHOT_FOLDER) if f.startswith("screenshot_") and f.endswith(".jpg")]
        if len(files) >= SCREENSHOT_MAX_COUNT:
            # Sort by modification time, oldest first
            files.sort(key=lambda x: os.path.getmtime(os.path.join(SCREENSHOT_FOLDER, x)))
            to_delete = len(files) - SCREENSHOT_MAX_COUNT + 1
            for i in range(to_delete):
                os.remove(os.path.join(SCREENSHOT_FOLDER, files[i]))
                logger.debug(f"Deleted old screenshot: {files[i]}")
    except Exception as e:
        logger.error(f"Error cleaning up screenshots: {e}")

def _take_screenshot():
    """Take a screenshot and save it with compression."""
    try:
        if SCREENSHOT_BACKEND == "pillow":
            screenshot = PILImageGrab.grab()
        elif SCREENSHOT_BACKEND == "pyscreenshot":
            screenshot = pyscreenshot.grab()
        else:
            raise RuntimeError("No screenshot backend available")

        # Ensure we have RGB color data (avoid grayscale/monochrome renders)
        if screenshot.mode != "RGB":
            screenshot = screenshot.convert("RGB")

        # Compress: save as JPEG
        timestamp = _now_timestamp()
        filename = f"screenshot_{timestamp}.jpg"
        filepath = os.path.join(SCREENSHOT_FOLDER, filename)

        # Save with compression
        screenshot.save(filepath, "JPEG", quality=SCREENSHOT_QUALITY, optimize=True)

        logger.debug(f"Screenshot saved: {filename}")

        # Upload screenshot file to the server
        if AGENT_ID:
            try:
                upload_screenshot(AGENT_ID, filepath)
            except Exception as e:
                logger.error(f"Error uploading screenshot: {e}")

        # Cleanup old ones
        _cleanup_old_screenshots()

    except Exception as e:
        logger.exception(f"Error taking screenshot with backend '{SCREENSHOT_BACKEND}': {e}")

def _screenshot_loop():
    """Main loop for taking screenshots at intervals."""
    while not STOP_EVENT.is_set():
        _take_screenshot()
        time.sleep(SCREENSHOT_INTERVAL)

# =========================
# PUBLIC API
# =========================
def start_screenshot(agent_id: str) -> Optional[threading.Thread]:
    """Start the screenshot service."""
    global AGENT_ID, SCREENSHOT_THREAD
    AGENT_ID = agent_id

    if SCREENSHOT_BACKEND is None or Image is None:
        logger.error("No screenshot backend available. Screenshot service disabled.")
        return None

    if SCREENSHOT_THREAD is not None and SCREENSHOT_THREAD.is_alive():
        logger.info("Screenshot service already running.")
        return SCREENSHOT_THREAD

    STOP_EVENT.clear()

    _ensure_folder()

    logger.info(
        f"Screenshot service starting -> {SCREENSHOT_FOLDER} "
        f"(interval: {SCREENSHOT_INTERVAL}s, max: {SCREENSHOT_MAX_COUNT}, backend: {SCREENSHOT_BACKEND})"
    )

    thread = threading.Thread(target=_screenshot_loop, daemon=True)
    thread.start()
    SCREENSHOT_THREAD = thread
    return thread

def stop_screenshot():
    """Stop the screenshot service."""
    STOP_EVENT.set()
    logger.info("Screenshot service stopped.")
