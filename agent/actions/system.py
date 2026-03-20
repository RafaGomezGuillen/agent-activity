import platform
import socket
import psutil
import os
import time
import re, uuid
from datetime import datetime

def get_basic_info():
    """
    Collect basic system information for agent registration.
    """
    try:
        cpu_freq = psutil.cpu_freq()
        return {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": f"{cpu_freq.max:.2f}" if cpu_freq else "N/A", # mHz
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "mac_address": ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        }
    except Exception as e:
        return {"error": str(e)}

def get_metrics():
    """
    Real time system metrics for heartbeat reporting.
    """
    # Memory
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disk
    disk = psutil.disk_usage("/")
    
    # Network
    net_before = psutil.net_io_counters()
    net_after = psutil.net_io_counters()

    battery = psutil.sensors_battery()

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": {
            "usage_percent": psutil.cpu_percent(interval=None),
            "per_cpu": psutil.cpu_percent(percpu=True),
            "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else "N/A"
        },
        "memory": {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_percent": mem.percent,
            "swap_used_percent": swap.percent
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_percent": disk.percent,
            "read_bytes": psutil.disk_io_counters().read_bytes,
            "write_bytes": psutil.disk_io_counters().write_bytes
        },
        "network": {
            "bytes_sent_total": net_after.bytes_sent,
            "bytes_recv_total": net_after.bytes_recv,
            "upload_speed_kb": round((net_after.bytes_sent - net_before.bytes_sent) / 1024, 2)
        },
        "battery": {
            "percent": battery.percent if battery else "N/A",
            "plugged": battery.power_plugged if battery else "N/A"
        },
        "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 2),
        "process_count": len(psutil.pids())
    }
