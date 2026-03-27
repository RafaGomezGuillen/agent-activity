import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Agent

logger = logging.getLogger("agent_job")

def check_agents_status():
    """
    Mark agents as offline if last_seen > 5 minutes
    """

    db: Session = SessionLocal()
    minutes = 5

    try:
        threshold = datetime.utcnow() - timedelta(minutes=minutes)

        updated = (
            db.query(Agent)
            .filter(Agent.last_seen < threshold, Agent.status == True)
            .update({Agent.status: False}, synchronize_session=False)
        )

        db.commit()

        if updated:
            logger.info(f"[CRON] Marked {updated} agents as offline")
    except Exception as e:
        logger.error(f"[CRON ERROR] {e}")
    finally:
        db.close()