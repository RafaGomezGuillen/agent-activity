"""
Linux daemon entry point for the agent.

Runs as a background systemd service
- systemctl stop / systemctl disable can properly terminate the process.
"""

import multiprocessing
import signal
import sys
import threading

from app.agent import Agent
from app.bootstrap import init_agent
from config.settings import APP_NAME
from core.single_instance import linux_single_instance
from logger import logger


def main():
    lock = linux_single_instance()
    if lock is None:
        logger.info(f"{APP_NAME} is already running. Exiting.")
        sys.exit(0)

    stop_event = threading.Event()

    def handle_signal(signum, frame):
        logger.info(f"Received signal {signum}, stopping {APP_NAME}...")
        stop_event.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        agent_id = init_agent()
        agent = Agent(agent_id)
        agent.run(stop_event=stop_event)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        sys.exit(1)
    finally:
        lock.close()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
