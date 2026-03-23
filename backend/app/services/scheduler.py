import logging
from apscheduler.schedulers.background import BackgroundScheduler

from app.services.agents import check_agents_status

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler.add_job(
        check_agents_status,
        trigger="interval",
        minutes=5,
        id="agent_status_job",
        replace_existing=True,
    )

    logger.info("--- Starting scheduler ---")
    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("--- Scheduler stopped ---")