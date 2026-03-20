import time

from actions.system import get_metrics
from api.client import send_metrics
from config.settings import METRICS_INTERVAL

class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def metrics(self):
        metrics = get_metrics()
        send_metrics(self.agent_id, metrics)
        print(f"[+] Metrics: {metrics}")

    def run(self):
        while True:
            try:
                self.metrics()
            except Exception as e:
                print(f"[!] Metrics error: {e}")

            time.sleep(METRICS_INTERVAL)