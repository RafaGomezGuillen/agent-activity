import logging
import os
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to console output"""

    COLORS = {
        'DEBUG': '\033[93m',  # Yellow
        'INFO': '\033[92m',   # Green
        'ERROR': '\033[91m',  # Red
        'RESET': '\033[0m'    # Reset
    }

    def format(self, record):
        message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{color}{message}{self.COLORS['RESET']}"

def setup_logging():
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, 'logs.log')

    # Create rotating file handler
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=4
    )

    # Set formatter for file (no colors)
    file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(file_formatter)

    # Get root logger and configure
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)