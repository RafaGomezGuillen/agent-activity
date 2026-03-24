import os
import logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create logger
logger = logging.getLogger('agent')
logger.setLevel(logging.DEBUG)

# File handler with rotation
file_handler = RotatingFileHandler(
    'logs/logs.log',
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=3  # Max 4 files total (original + 3 backups)
)

def namer(name):
    if '.log.' in name:
        base, num = name.rsplit('.log.', 1)
        return f"{base}_{num}.log"
    return name

file_handler.namer = namer

file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            color = Fore.YELLOW
        elif record.levelno == logging.INFO:
            color = Fore.GREEN
        elif record.levelno == logging.ERROR:
            color = Fore.RED
        else:
            color = Fore.WHITE
        record.msg = color + str(record.msg) + Style.RESET_ALL
        return super().format(record)

console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def error(message):
    logger.error(message)

__all__ = ['logger', 'debug', 'info', 'error']