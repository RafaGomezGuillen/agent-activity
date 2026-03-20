from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AgentBase(BaseModel):
    id: str
    
    hostname: str
    os: str
    os_release: Optional[str] = None
    os_version: Optional[str] = None
    architecture: Optional[str] = None
    processor: Optional[str] = None

    physical_cores: int
    total_cores: int
    max_frequency: Optional[str] = None

    ip_address: str
    mac_address: str

class AgentCreate(AgentBase):
    id: Optional[str] = None # type: ignore

class AgentOut(AgentBase):
    id: str
    status: bool
    created_at: datetime
    last_seen: datetime

    class Config:
        from_attributes = True

class AgentPagination(BaseModel):
    total: int
    page: int
    size: int
    items: List[AgentOut]