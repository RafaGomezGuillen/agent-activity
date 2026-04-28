from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models import Agent, Metric
from app.schemas.metrics import MetricsCreate, MetricsPagination

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.post("/{agent_id}", response_model=dict)
def ingest_metrics(
    agent_id: str,
    data: MetricsCreate,
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.last_seen = datetime.utcnow()
    agent.status = True

    metrics = Metric(
        agent_id=agent_id,

        cpu_usage=data.cpu.usage_percent,

        memory_used_percent=data.memory.used_percent,
        memory_total_gb=data.memory.total_gb,
        memory_available_gb=data.memory.available_gb,

        disk_used_percent=data.disk.used_percent,
        disk_total_gb=data.disk.total_gb,

        bytes_sent_total=data.network.bytes_sent_total,
        bytes_recv_total=data.network.bytes_recv_total,
        packets_sent_total=data.network.packets_sent_total,
        packets_recv_total=data.network.packets_recv_total,
        upload_speed_kb=data.network.upload_speed_kb,
        download_speed_kb=data.network.download_speed_kb,

        uptime_hours=data.uptime_hours,
        process_count=data.process_count,
        current_app=data.current_app,

        battery_percent=data.battery.percent,
        battery_plugged=str(data.battery.plugged)
    )

    db.add(metrics)
    db.commit()

    return {"status": "ok"}

@router.get("/{agent_id}", response_model=MetricsPagination)
def get_metrics(
    agent_id: str,
    db: Session = Depends(get_db),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
):
    query = db.query(Metric).filter(
        Metric.agent_id == agent_id
    )

    if start_time:
        query = query.filter(Metric.timestamp >= start_time)

    if end_time:
        query = query.filter(Metric.timestamp <= end_time)

    total = query.count()

    results = (
        query.order_by(Metric.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": results
    }
