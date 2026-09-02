# Testing Guide

## Running Tests

### All Tests
```bash
pytest
```

### Specific Test File
```bash
pytest tests/test_api.py -v
```

### With Coverage
```bash
pytest --cov=unified_manager tests/
```

## Test Structure
- `tests/test_api.py` - API endpoint tests
- `tests/test_database.py` - Database operation tests
- `conftest.py` - Pytest fixtures

## Writing Tests
```python
def test_example():
    response = client.get("/api/health")
    assert response.status_code == 200
```

## Docker Testing
```bash
docker-compose -f docker-compose.test.yml up
```
