import platform
import time
from tokenize import Name

from config.settings import APP_CACHE_TTL, LAST_APP_CHECK

SYSTEM = platform.system()

def get_current_app():
    """
    Get the name of the currently active application/window.
    Uses caching to avoid excessive system calls, refreshing every APP_CACHE_TTL seconds.
    Returns:
        str: Name of the active application or "unknown" if it cannot be determined
    """
    global CURRENT_APP, LAST_APP_CHECK

    now = time.time()

    if now - LAST_APP_CHECK > APP_CACHE_TTL:
        CURRENT_APP = _get_active_window()
        LAST_APP_CHECK = now

    return CURRENT_APP


def _get_active_window():
    """
    Get the name of the currently active window.
    Returns:
        str: Name of the active window or "unknown" if it cannot be determined
    """
    try:
        if SYSTEM == "Darwin":
            return _get_active_window_macos()
        elif SYSTEM == "Windows":
            return _get_active_window_windows()
        elif SYSTEM == "Linux":
            return _get_active_window_linux()
    except Exception:
        return "unknown"

    return "unknown"

def _get_active_window_macos():
    """
    Get the name of the currently active application on macOS using AppleScript.
    Returns:
        str: Name of the active application or "unknown" if it cannot be determined
    """
    try:
        import subprocess
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    
    return "unknown"
    
def _get_active_window_windows():
    """
    Get the name of the currently active window on Windows using ctypes.
    Returns:
        str: Name of the active window or "unknown" if it cannot be determined
    """
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    
    if not hwnd:
        return None

    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value
    
    return "unknown"

def _get_active_window_linux():
    """
    Get the name of the currently active window on Linux using xdotool.
    Returns:
        str: Name of the active window or "unknown" if it cannot be determined
    """
    import subprocess

    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return "unknown"