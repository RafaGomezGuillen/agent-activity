from app.bootstrap import init_agent
from app.agent import Agent

def main():
    agent_id = init_agent()

    # main loop
    agent = Agent(agent_id)
    agent.run()


if __name__ == "__main__":
    main()
