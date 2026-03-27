import os
import mimetypes
from pathlib import Path
from datetime import datetime

from config.settings import MAX_FILE_SIZE

def list_directory(path: str):
    """
    List directory recursively (1 level)
    """
    result = []

    try:
        p = Path(path)

        if not p.exists():
            return {"error": "Path not found"}

        for item in p.iterdir():
            stat = item.stat()

            result.append({
                "name": item.name,
                "path": str(item.resolve()),
                "is_dir": item.is_dir(),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

        # Schema expects a JSON object for command result, not a raw list.
        return {"entries": result}

    except Exception as e:
        return {"error": str(e)}

def read_file(path: str):
    """
    Read file content (safe)
    """
    try:
        if not os.path.exists(path):
            return {"error": "File not found"}

        size = os.path.getsize(path)

        if size > MAX_FILE_SIZE:
            return {"error": "File too large"}

        mime, _ = mimetypes.guess_type(path)

        # Only text
        if mime and not mime.startswith("text"):
            return {"error": "Not a readable text file"}

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "path": path,
            "size": size,
            "content": content
        }

    except Exception as e:
        return {"error": str(e)}
