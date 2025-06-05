import os
import json
from typing import List, Dict, Any, Optional
from utils.json_handler import read_json, write_json

class BaseRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the data file and directory exist"""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        if not os.path.exists(self.file_path):
            write_json(self.file_path, [])
            print(f"Created new data file: {self.file_path}")
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all items from the JSON file"""
        try:
            data = read_json(self.file_path)
            print(f"Loaded {len(data)} items from {self.file_path}")
            return data
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return []
    
    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get item by ID"""
        items = self.get_all()
        return next((item for item in items if item.get('id') == item_id), None)
    
    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item"""
        items = self.get_all()
        items.append(item)
        success = write_json(self.file_path, items)
        if success:
            print(f"Created new item with id: {item.get('id')}")
        else:
            print(f"Failed to save item to {self.file_path}")
        return item
    
    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing item"""
        items = self.get_all()
        for i, item in enumerate(items):
            if item.get('id') == item_id:
                items[i] = {**item, **data}
                write_json(self.file_path, items)
                print(f"Updated item with id: {item_id}")
                return items[i]
        return None
    
    def delete(self, item_id: str) -> bool:
        """Delete an item"""
        items = self.get_all()
        original_length = len(items)
        items = [item for item in items if item.get('id') != item_id]
        
        if len(items) < original_length:
            write_json(self.file_path, items)
            print(f"Deleted item with id: {item_id}")
            return True
        return False