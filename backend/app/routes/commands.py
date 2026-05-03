from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import Optional, List

from app.db.database import get_db
from app.models import Command, Agent
from app.schemas.commands import CommandCreate, CommandOut, CommandUpdate, CommandPagination

router = APIRouter(prefix="/commands", tags=["Commands"])

@router.post("/", response_model=CommandOut, status_code=status.HTTP_201_CREATED)
def create_command(data: CommandCreate, db: Session = Depends(get_db)):
    """
    Create a new command for an agent.
    structure:
    {"agent_id": "<id>", "command": "filesystem.read_file", "params": {"path": "/etc/hosts"}}
    {"agent_id": "<id>", "command": "filesystem.list_directory", "params": {"path": "/etc/logstash/pipelines"}}
    """
    new_command = Command(
        agent_id=data.agent_id,
        command=data.command,
        params=data.params or {}
    )

    agent_exists = db.query(Agent).filter(Agent.id == data.agent_id).first()
    
    if not agent_exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent_exists.status == False:
        raise HTTPException(status_code=400, detail="Agent is not active")
    
    if new_command.command not in Command.AVAILABLE_COMMANDS:
        raise HTTPException(status_code=400, detail="Invalid command type")

    db.add(new_command)
    db.commit()
    db.refresh(new_command)

    return new_command

@router.get("/{agent_id}", response_model=List[CommandOut])
def get_pending_commands(
    agent_id: str = Path(..., description="Unique ID of the agent"),
    db: Session = Depends(get_db)
):
    """
    Get pending commands for an agent.
    """
    agent_exists = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent_exists:
        raise HTTPException(status_code=404, detail="Agent not found")

    commands = db.query(Command).filter(
        and_(Command.agent_id == agent_id, Command.status == "pending")
    ).order_by(Command.created_at).all()

    return commands

@router.put("/{command_id}", response_model=CommandOut)
def update_command(
    command_id: str = Path(..., description="Unique ID of the command"),
    data: CommandUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Update a command's status and result.
    """
    command = db.query(Command).filter(Command.id == command_id).first()

    if not command:
        raise HTTPException(status_code=404, detail="Command not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(command, key, value)

    if data.status in ["executed", "failed"]:
        command.executed_at = datetime.utcnow()

    db.commit()
    db.refresh(command)

    return command

@router.get("/", response_model=CommandPagination)
def list_commands(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (eg: pending, executed, failed)"),
    limit: int = Query(100, ge=1, le=1000, description="Limit must be between 1 and 1000"),
    offset: int = Query(0, ge=0, description="Offset must be non-negative"),
    db: Session = Depends(get_db)
):
    """
    List all commands with optional filters.
    """
    query = db.query(Command)

    if agent_id:
        query = query.filter(Command.agent_id == agent_id)

    if status_filter:
        query = query.filter(Command.status == status_filter)

    total = query.count()

    results = (
        query.order_by(Command.created_at.desc())
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

@router.delete("/{command_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_command(
    agent_id: str = Path(..., description="ID of the agent to delete commands for"),
    command_id: str = Path(..., description="Unique ID of the command"),
    db: Session = Depends(get_db)
):
    """
    Delete a command by ID.
    """
    agent_exists = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent_exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    command = db.query(Command).filter(
        and_(Command.id == command_id, Command.agent_id == agent_id)
    ).first()

    if not command:
        raise HTTPException(status_code=404, detail="Command not found")

    db.delete(command)
    db.commit()