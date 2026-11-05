"""
Safe I/O Utility with Atomic File Writes and Schema Validation.
Designed for Windows NTFS robustness and high reliability.
"""

import os
import json
import time
import tempfile
from typing import Any, Dict, Optional
import jsonschema

def atomic_write_text(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """
    Safely writes text to a file using a temporary file and atomic replacement.
    Retries up to 5 times on Windows in case of transient NTFS file locks.
    """
    abs_path = os.path.abspath(filepath)
    dir_name = os.path.dirname(abs_path)
    os.makedirs(dir_name, exist_ok=True)
    
    prefix = f".{os.path.basename(abs_path)}.tmp_"
    tmp_fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=prefix)
    try:
        with os.fdopen(tmp_fd, "w", encoding=encoding) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        
        # Retry loop for Windows file locking
        max_retries = 5
        for attempt in range(max_retries):
            try:
                os.replace(tmp_path, abs_path)
                break
            except PermissionError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.05 * (attempt + 1))
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

def atomic_write_json(filepath: str, data: Any, schema_path: Optional[str] = None, indent: int = 2) -> None:
    """
    Serializes data to JSON, validates against schema if provided, and atomically writes to disk.
    """
    if schema_path and os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
        jsonschema.validate(instance=data, schema=schema)
    
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    atomic_write_text(filepath, json_str + "\n")

def read_json(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Safely reads JSON file with UTF-8 encoding.
    Returns None if file does not exist.
    """
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def read_text(filepath: str) -> Optional[str]:
    """
    Safely reads text file with UTF-8 encoding.
    Returns None if file does not exist.
    """
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
