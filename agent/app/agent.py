import time

from actions.system import get_metrics
from api.client import send_metrics
from config.settings import METRICS_INTERVAL
from logger import logger

class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def metrics(self):
        metrics = get_metrics()
        send_metrics(self.agent_id, metrics)
        logger.info(f"Metrics: {metrics}")

    def run(self):
        while True:
            try:
                self.metrics()
            except Exception as e:
                logger.error(f"Metrics error: {e}")

            time.sleep(METRICS_INTERVAL)