import os
import tempfile
from pathlib import Path

try:
    import fcntl
except ImportError:
    fcntl = None


class SingleInstance:
    """Prevent multiple agent instances from running simultaneously."""

    def __init__(self, name: str = "alisium-agent"):
        self.name = name
        self.lock_file_path = Path(tempfile.gettempdir()) / f"{self.name}.lock"
        self.lock_file = None

    def acquire(self) -> bool:
        """Try to acquire an exclusive lock. Returns True if acquired."""
        self.lock_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file = open(self.lock_file_path, "w+")
        self.lock_file.write(str(os.getpid()))
        self.lock_file.flush()

        if fcntl is None:
            return True

        try:
            fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def release(self) -> None:
        """Release the lock file."""
        try:
            if self.lock_file is None:
                return

            if fcntl is not None:
                fcntl.flock(self.lock_file, fcntl.LOCK_UN)

            self.lock_file.close()
            self.lock_file = None

            if self.lock_file_path.exists():
                self.lock_file_path.unlink()
        except Exception:
            pass
