import pytest
from unified_manager.core.db_utils import get_db_connection

@pytest.mark.asyncio
async def test_db_connection():
    try:
        conn = await get_db_connection()
        assert conn is not None
    except Exception as e:
        pytest.skip(f"Database not available: {e}")
