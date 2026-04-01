import psutil
from datetime import datetime


def list_processes():
    """
    Get all running processes in a structured way
    """
    processes = []

    for proc in psutil.process_iter([
        "pid",
        "name",
        "username",
        "cpu_percent",
        "memory_percent",
        "create_time"
    ]):
        try:
            info = proc.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "user": info["username"],
                "cpu": info["cpu_percent"],
                "memory": round(info["memory_percent"], 2) if info["memory_percent"] is not None else None,
                "started_at": datetime.fromtimestamp(
                    info["create_time"]
                ).isoformat() if info["create_time"] else None
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes
