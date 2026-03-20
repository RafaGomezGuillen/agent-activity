import os
from config.settings import AGENT_FILE

def save_agent_id(agent_id):
    """Save agent ID to persistent storage.
    
    Args:
        agent_id (str): Unique agent identifier to save
    """
    with open(AGENT_FILE, "w") as f:
        f.write(agent_id)

def load_agent_id():
    """Load agent ID from persistent storage.
    
    Returns:
        str: Agent ID if file exists, None otherwise
    """
    if not os.path.exists(AGENT_FILE):
        return None

    with open(AGENT_FILE, "r") as f:
        return f.read().strip()
