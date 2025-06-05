import json
import os
from typing import Any, Dict, List, Union

def read_json(file_path: str) -> Union[List, Dict[str, Any]]:
    """Read JSON data from file with error handling"""
    try:
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def write_json(file_path: str, data: Union[List, Dict[str, Any]]) -> bool:
    """Write JSON data to file with error handling"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False