import time

from logger import logger
from actions.system import get_metrics
from app.command_handlers import execute_command
from api.client import send_metrics, fetch_commands, update_command
from config.settings import METRICS_INTERVAL
from requests.exceptions import HTTPError

class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def metrics(self):
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

    def run(self):
        while True:
            try:
                self.metrics()
                self.check_commands()
            except Exception as e:
                logger.error(f"Main loop error: {e}")

            time.sleep(METRICS_INTERVAL)