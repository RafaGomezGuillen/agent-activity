from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional

from app.db.database import get_db
from app.models import Agent
from app.schemas.agents import AgentCreate, AgentOut, AgentPagination

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.post("/register", response_model=AgentOut, status_code=status.HTTP_200_OK)
def register_agent(data: AgentCreate, db: Session = Depends(get_db)):
    """
    Register agent. If agent exists (same ID), return existing.
    """

    agent = db.query(Agent).filter(Agent.id == data.id).first()

    if agent:
        for key, value in data.model_dump().items():
            setattr(agent, key, value)

        agent.last_seen = datetime.utcnow() # type: ignore
        agent.status = True # type: ignore

        db.commit()
        db.refresh(agent)

        return agent

    new_agent = Agent(
        **data.model_dump(),
        status=True
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent

@router.get("/", response_model=AgentPagination)
def list_agents(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    os_filter: Optional[str] = Query(None, alias="os", description="Filter by OS"),
    status_filter: Optional[bool] = Query(None, alias="status", description="Filter by status (True=online, False=offline)"),
):
    """
    List agents with pagination, search and filters.
    """

    query = db.query(Agent)

    if search:
        query = query.filter(
            or_(
                Agent.hostname.ilike(f"%{search}%"),
                Agent.ip_address.ilike(f"%{search}%"),
                Agent.mac_address.ilike(f"%{search}%"),
            )
        )

    if os_filter:
        query = query.filter(Agent.os == os_filter)

    if status_filter is not None:
        query = query.filter(Agent.status == status_filter)

    total = query.count()

    offset = (page - 1) * size

    agents = (
        query.order_by(Agent.last_seen.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": agents
    }

@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: str, db: Session = Depends(get_db)):

    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.delete(agent)
    db.commit()

    return None