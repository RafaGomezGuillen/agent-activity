from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class Clipboard(Base):
    __tablename__ = "clipboards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    app = Column(String, index=True)

    value = Column(Text)

    # Relationships
    agent_id = Column(String, ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    agent = relationship("Agent", back_populates="clipboards")