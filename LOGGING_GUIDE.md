# Logging Guide

## Overview
The project uses structured logging with rotation support.

## Configuration
Logging is configured in `logging_config.py`:
- **Level**: INFO, DEBUG, WARNING, ERROR, CRITICAL
- **Format**: Standard or JSON
- **Rotation**: Size-based (10MB max, 5 backups)

## Usage
```python
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Message")
logger.error("Error occurred", extra={"task_id": 123})
```

## Log Files
- Location: `logs/` directory
- Rotation: Automatic when file exceeds 10MB
- Retention: 5 backup files
