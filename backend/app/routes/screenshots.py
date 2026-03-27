import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.database import get_db
from app.models.screenshot import Screenshot
from app.models.agent import Agent
from app.schemas.screenshots import ScreenshotPagination

UPLOAD_DIR = "uploads/screenshots"

router = APIRouter(prefix="/screenshots", tags=["Screenshots"])

def _ensure_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{agent_id}")
def upload_screenshot(
    agent_id: str = Path(..., description="Unique ID of the agent sending the screenshot"),
    file: UploadFile = File(..., description="Screenshot file to upload"),
    db: Session = Depends(get_db)
):
    """
    Upload a screenshot for a specific agent.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    _ensure_dir()

    filename = f"{agent_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    screenshot = Screenshot(
        agent_id=agent_id,
        filename=filename,
        filepath=filepath
    )

    db.add(screenshot)
    db.commit()

    return {"status": "uploaded"}

@router.get("/", response_model=ScreenshotPagination)
def list_screenshots(
    db: Session = Depends(get_db),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    start_time: Optional[datetime] = Query(None, description="Filter by start time"),
    end_time: Optional[datetime] = Query(None, description="Filter by end time"),
    limit: int = Query(50, le=200, description="Limit must be 200 or less"),
    offset: int = Query(0, description="Offset must be non-negative")
):
    """
    List screenshots with optional filtering.
    """
    query = db.query(Screenshot)

    if agent_id:
        query = query.filter(Screenshot.agent_id == agent_id)

    if start_time:
        query = query.filter(Screenshot.created_at >= start_time)

    if end_time:
        query = query.filter(Screenshot.created_at <= end_time)

    total = query.count()

    items = (
        query.order_by(Screenshot.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }

@router.get("/agent/{agent_id}", response_model=ScreenshotPagination)
def get_agent_screenshots(
    agent_id: str = Path(..., description="ID of the agent to retrieve screenshots for"),
    db: Session = Depends(get_db),
    start_time: Optional[datetime] = Query(None, description="Filter by start time"),
    end_time: Optional[datetime] = Query(None, description="Filter by end time"),
    limit: int = Query(50, le=200, description="Limit must be 200 or less"),
    offset: int = Query(0, description="Offset must be non-negative")
):
    """
    Get screenshots for a specific agent.
    """
    query = db.query(Screenshot).filter(
        Screenshot.agent_id == agent_id
    )

    if start_time:
        query = query.filter(Screenshot.created_at >= start_time)

    if end_time:
        query = query.filter(Screenshot.created_at <= end_time)

    total = query.count()

    items = (
        query.order_by(Screenshot.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }

@router.get("/file/{screenshot_id}")
def get_screenshot_file(
    screenshot_id: str = Path(..., description="ID of the screenshot to retrieve"),
    db: Session = Depends(get_db)
):
    screenshot = db.query(Screenshot).filter(
        Screenshot.id == screenshot_id
    ).first()

    if not screenshot:
        raise HTTPException(status_code=404, detail="Not found")

    return FileResponse(screenshot.filepath)

@router.delete("/{screenshot_id}")
def delete_screenshot(
    screenshot_id: str = Path(..., description="ID of the screenshot to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a screenshot.
    """
    screenshot = db.query(Screenshot).filter(
        Screenshot.id == screenshot_id
    ).first()

    if not screenshot:
        raise HTTPException(status_code=404, detail="Not found")

    # Delete the file from disk
    if os.path.exists(screenshot.filepath):
        os.remove(screenshot.filepath)

    db.delete(screenshot)
    db.commit()

    return {"status": "deleted"}