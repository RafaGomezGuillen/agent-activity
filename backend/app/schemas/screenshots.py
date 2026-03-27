from pydantic import BaseModel
from datetime import datetime
from typing import List


class ScreenshotOut(BaseModel):
    id: str
    agent_id: str
    filename: str
    uri: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScreenshotPagination(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[ScreenshotOut]