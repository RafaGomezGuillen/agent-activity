"""
macOS Menu Bar app

Provides Start / Stop / Force Quit controls from the status bar icon.
The agent runs in a background thread; the rumps event loop owns the main thread.
"""

import sys
import threading
import rumps

from config.settings import APP_NAME, ICON_PATH
from app.bootstrap import init_agent
from app.agent import Agent
from core.single_instance import SingleInstance
from logger import logger


class MacAgent(rumps.App):

    def __init__(self):
        super().__init__(APP_NAME, icon=ICON_PATH, quit_button=None)

        self._stop_event = threading.Event()
        self._agent_id = None
        self._running = False

        self.menu = [
            rumps.MenuItem("🏃 Start Agent", callback=self.start_agent),
            rumps.MenuItem("🛑 Stop Agent", callback=self.stop_agent),
            None,  # separator
            rumps.MenuItem("❌ Force Quit", callback=self.force_quit),
        ]

    # ------------------------------------------------------------------
    # Menu callbacks
    # ------------------------------------------------------------------

    def start_agent(self, _):
        if self._running:
            rumps.notification(APP_NAME, "Already running", "The agent is already running.")
            return

        self._stop_event.clear()
        self._running = True
        thread = threading.Thread(target=self._run_agent, daemon=True)
        thread.start()
        logger.info("Agent started from menu bar.")
        rumps.notification(APP_NAME, "Agent Started", "The agent is now running in the background.")

    def stop_agent(self, _):
        if not self._running:
            rumps.notification(APP_NAME, "Not running", "The agent is not currently running.")
            return

        self._stop_event.set()
        self._running = False
        logger.info("Agent stopped from menu bar.")
        rumps.notification(APP_NAME, "Agent Stopped", "The agent has been stopped.")
    
    def force_quit(self, _):
        self._stop_event.set()
        logger.info("Agent force quit from menu bar.")
        rumps.notification(APP_NAME, "Exiting", "The application will now exit.")
        rumps.quit_application()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run_agent(self):
        try:
            if not self._agent_id:
                self._agent_id = init_agent()

            agent = Agent(self._agent_id)
            agent.run(stop_event=self._stop_event)

        except Exception as e:
            logger.error(f"Agent error: {e}")
        finally:
            self._running = False


if __name__ == "__main__":
    instance = SingleInstance(APP_NAME)

    if not instance.acquire():
        logger.error(f"Another instance of {APP_NAME} is already running.")
        sys.exit(1)

    try:
        MacAgent().run()
    finally:
        instance.release()
