import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Agent

logger = logging.getLogger("commands_job")

def check_pending_commands():
    """
    Mark pending commands as failed if created_at > 10 minutes
    """

    db: Session = SessionLocal()
    minutes = 10

    try:
        threshold = datetime.utcnow() - timedelta(minutes=minutes)

        updated = (
            db.query(Agent)
            .filter(Agent.created_at < threshold, Agent.status == "pending")
            .update({Agent.status: "failed"}, synchronize_session=False)
        )

        db.commit()

        if updated:
            logger.info(f"[CRON] Marked {updated} pending commands as failed")
    except Exception as e:
        logger.error(f"[CRON ERROR] {e}")
    finally:
        db.close()