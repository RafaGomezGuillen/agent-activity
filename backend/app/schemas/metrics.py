from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CpuSchema(BaseModel):
    usage_percent: float

class MemorySchema(BaseModel):
    used_percent: float
    total_gb: float
    available_gb: float

class DiskSchema(BaseModel):
    used_percent: float
    total_gb: float

class NetworkSchema(BaseModel):
    bytes_sent_total: float
    bytes_recv_total: float

class BatterySchema(BaseModel):
    percent: Optional[float]
    plugged: Optional[bool]

class MetricsCreate(BaseModel):
    cpu: CpuSchema
    memory: MemorySchema
    disk: DiskSchema
    network: NetworkSchema

    uptime_hours: float
    process_count: int
    current_app: str

    battery: BatterySchema

class MetricsOut(BaseModel):
    id: str
    agent_id: str
    timestamp: datetime

    cpu_usage: float
    memory_used_percent: float
    memory_total_gb: float
    memory_available_gb: float

    disk_used_percent: float
    disk_total_gb: float

    bytes_sent: float
    bytes_recv: float

    uptime_hours: float
    process_count: int

    battery_percent: Optional[float]
    battery_plugged: Optional[str]
    current_app: str

    class Config:
        from_attributes = True

class MetricsPagination(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[MetricsOut]