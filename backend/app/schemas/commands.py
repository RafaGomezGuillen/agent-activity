from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class CommandBase(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None

class CommandCreate(CommandBase):
    agent_id: str

class CommandOut(CommandBase):
    id: str
    agent_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommandUpdate(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None
    executed_at: Optional[datetime] = None


class CommandPagination(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[CommandOut]