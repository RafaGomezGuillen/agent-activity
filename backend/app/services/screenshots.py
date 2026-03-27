import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Screenshot

logger = logging.getLogger("screenshot_job")

def delete_old_screenshots():
    """
    Delete screenshots older than 7 days
    """

    db: Session = SessionLocal()
    days = 7

    try:
        threshold = datetime.utcnow() - timedelta(days=days)

        deleted = (
            db.query(Screenshot)
            .filter(Screenshot.created_at < threshold)
            .delete(synchronize_session=False)
        )

        db.commit()

        if deleted:
            logger.info(f"[CRON] Deleted {deleted} old screenshots")
    except Exception as e:
        logger.error(f"[CRON ERROR] {e}")
    finally:
        db.close()