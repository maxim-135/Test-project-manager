from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class DBUtils:
    """Database utility functions."""
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Sanitize user input for database queries."""
        if not isinstance(value, str):
            return str(value)
        # Remove potentially dangerous characters
        return value.replace("'", "''")
    
    @staticmethod
    def build_where_clause(filters: Dict[str, Any]) -> tuple:
        """Build WHERE clause for SQL queries."""
        conditions = []
        params = []
        for key, value in filters.items():
            conditions.append(f"{key} = ?")
            params.append(value)
        return " AND ".join(conditions), params
    
    @staticmethod
    def paginate(query: str, limit: int, offset: int) -> str:
        """Add pagination to SQL query."""
        return f"{query} LIMIT {limit} OFFSET {offset}"
