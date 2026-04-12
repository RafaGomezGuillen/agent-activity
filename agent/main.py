import sys

from config.settings import APP_NAME
from app.bootstrap import init_agent
from app.agent import Agent
from core.single_instance import SingleInstance
from logger import logger

def main():
    agent_id = init_agent()

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