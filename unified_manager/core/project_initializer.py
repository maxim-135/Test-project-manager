import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ProjectInitializer:
    """Initializes project structure and configuration."""
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist."""
        directories = [
            "unified_manager/data",
            "unified_manager/logs",
            "exports",
            "projects",
            "logs",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
    
    @staticmethod
    def init_config() -> Dict[str, Any]:
        """Initialize configuration from environment."""
        return {
            "db_type": os.getenv("DB_TYPE", "postgres"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "is_docker": os.getenv("IS_DOCKER", "false").lower() == "true",
        }
    
    @staticmethod
    def validate_environment() -> bool:
        """Validate that the environment is properly configured."""
        required_vars = ["DB_TYPE"]
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            logger.error(f"Missing required environment variables: {missing}")
            return False
        
        return True
