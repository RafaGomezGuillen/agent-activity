from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class Command(Base):
    __tablename__ = "commands"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    agent_id = Column(String, ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    agent = relationship("Agent", back_populates="commands")

    command = Column(String, index=True)  # e.g., "filesystem.list_directory"
    params = Column(JSON)  # JSON parameters for the command

    status = Column(String, default="pending", index=True)  # pending, executed, failed
    result = Column(JSON, nullable=True)  # JSON result after execution

    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)

    AVAILABLE_COMMANDS = ["filesystem.list_directory", "filesystem.read_file"]