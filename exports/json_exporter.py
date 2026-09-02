import json
from typing import Any, Dict
from datetime import datetime


class JSONExporter:
    """Exports data to JSON format."""
    
    @staticmethod
    def export(data: Dict[str, Any], filepath: str) -> None:
        """Export data to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    @staticmethod
    def to_string(data: Dict[str, Any]) -> str:
        """Convert data to JSON string."""
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
