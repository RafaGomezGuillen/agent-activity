from config.settings import SCREENSHOT_FOLDER
from actions.screenshot import start_screenshot
from logger import logger

def start_screenshot_service(agent_id):
    """Start the screenshot service in a background thread."""
    try:
        if agent_id is None:
            logger.error("No agent ID found. Screenshot service will not start.")
            return

        thread = start_screenshot(agent_id)

        if thread is None:
            logger.error("Screenshot service disabled.")
        else:
            logger.info(f"Screenshot service running → {SCREENSHOT_FOLDER}")

    except Exception as e:
        logger.error(f"Screenshot service error: {e}")