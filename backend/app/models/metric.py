from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from datetime import datetime
import uuid

from sqlalchemy.orm import relationship

from app.db.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # CPU
    cpu_usage = Column(Float)
    
    # Memory
    memory_used_percent = Column(Float)
    memory_total_gb = Column(Float)
    memory_available_gb = Column(Float)

    # Disk
    disk_used_percent = Column(Float)
    disk_total_gb = Column(Float)

    # Network
    bytes_sent = Column(Float)
    bytes_recv = Column(Float)

    # System
    uptime_hours = Column(Float)
    process_count = Column(Integer)
    current_app = Column(String)

    # Battery
    battery_percent = Column(Float, nullable=True)
    battery_plugged = Column(String, nullable=True)

    # Relationships
    agent_id = Column(String, ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    agent = relationship("Agent", back_populates="metrics")