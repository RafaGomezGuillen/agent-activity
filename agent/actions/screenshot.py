import os
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

try:
    import pyscreenshot as ImageGrab
    from PIL import Image
except ImportError:
    ImageGrab = None
    Image = None

logger = logging.getLogger("screenshot")
logging.basicConfig(level=logging.INFO)

# =========================
# STATE
# =========================
AGENT_ID = None
STOP_EVENT = threading.Event()

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
        # Grab screenshot (PIL Image object)
        screenshot = ImageGrab.grab()

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
        logger.error(f"Error taking screenshot: {e}")

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
    global AGENT_ID
    AGENT_ID = agent_id

    if ImageGrab is None or Image is None:
        logger.error("pyscreenshot or Pillow not installed. Screenshot service disabled.")
        return None

    _ensure_folder()

    logger.info(f"Screenshot service starting -> {SCREENSHOT_FOLDER} (interval: {SCREENSHOT_INTERVAL}s, max: {SCREENSHOT_MAX_COUNT})")

    thread = threading.Thread(target=_screenshot_loop, daemon=True)
    thread.start()
    return thread

def stop_screenshot():
    """Stop the screenshot service."""
    STOP_EVENT.set()
    logger.info("Screenshot service stopped.")