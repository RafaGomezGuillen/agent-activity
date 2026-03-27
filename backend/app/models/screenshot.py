from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
import uuid

from sqlalchemy.orm import relationship

from app.db.database import Base

class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    filename = Column(String)
    filepath = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    agent_id = Column(String, ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    agent = relationship("Agent", back_populates="screenshots")

    @property
    def uri(self):
        return f"/screenshots/file/{self.id}"