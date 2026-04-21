import os

from config.settings import APP_NAME

WINDOWS_MUTEX = f"Local\\{APP_NAME}-single-instance"
LINUX_LOCK_FILE = f"/tmp/{APP_NAME}.lock"


def linux_single_instance():
    """
    Acquire an exclusive lock file to enforce a single instance on Linux.
    """
    import fcntl

    lock_file = open(LINUX_LOCK_FILE, "w")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_file.write(str(os.getpid()))
        lock_file.flush()
        return lock_file
    except OSError:
        lock_file.close()
        return None


def another_mac_instance_running() -> bool:
    """
    Check if another instance of the application is already running on macOS.
    """
    from AppKit import NSRunningApplication
    from Foundation import NSBundle

    bundle_id = NSBundle.mainBundle().bundleIdentifier()
    if not bundle_id:
        return False

    current_pid = os.getpid()
    running = NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle_id)

    for app in running:
        if app.processIdentifier() != current_pid:
            return True

    return False

def windows_single_instance():
    """
    Acquire a named Windows mutex for the tray app instance.
    """
    import win32api
    import win32event
    import winerror

    mutex = win32event.CreateMutex(None, False, WINDOWS_MUTEX)

    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        return None

    return mutex
