from actions.system import get_basic_info
from api.client import register_agent
from storage.identity import load_agent_id, save_agent_id
from logger import logger

def init_agent():
    agent_id = load_agent_id()

    if not agent_id:
        logger.info("Registering agent...")
        info = get_basic_info()
        agent_id = register_agent(info)
        save_agent_id(agent_id)
        logger.info(f"Registered with ID: {agent_id}")
    else:
        logger.debug(f"Loaded existing agent ID: {agent_id}")

    return agent_id