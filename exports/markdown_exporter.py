import markdown
from typing import Any, Dict
from datetime import datetime


class MarkdownExporter:
    """Exports data to Markdown format."""
    
    @staticmethod
    def export(data: Dict[str, Any], filepath: str) -> None:
        """Export data to Markdown file."""
        content = MarkdownExporter.to_markdown(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def to_markdown(data: Dict[str, Any]) -> str:
        """Convert data to Markdown string."""
        lines = ["# Export Report", f"Generated: {datetime.now().isoformat()}", ""]
        
        if isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"## {key}")
                lines.append(f"```\n{value}\n```")
                lines.append("")
        else:
            lines.append(f"```\n{data}\n```")
        
        return "\n".join(lines)
