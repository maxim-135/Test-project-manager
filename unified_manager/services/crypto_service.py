import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class CryptoService:
    """Service for cryptographic operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a random token."""
        import secrets
        return secrets.token_urlsafe(length)
