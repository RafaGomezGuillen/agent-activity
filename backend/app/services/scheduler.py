from apscheduler.schedulers.background import BackgroundScheduler

from app.services.agents import check_agents_status

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        check_agents_status,
        trigger="interval",
        minutes=5,
        id="agent_status_job",
        replace_existing=True,
    )

    print("--- Starting scheduler ---")
    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("--- Scheduler stopped ---")