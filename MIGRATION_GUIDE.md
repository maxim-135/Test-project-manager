# Migration Guide

## Database Migrations

This project uses Alembic for database migrations.

### Running Migrations
```bash
# Run all migrations
python setup_migrations.py

# Or using Alembic CLI
alembic upgrade head
```

### Creating New Migrations
```bash
alembic revision --autogenerate -m "Description"
```

### Migration Files
- Location: `alembic/versions/`
- Initial migration: `001_initial.py`

## Database Schema
The project supports both:
- **PostgreSQL**: Production use
- **SQLite**: Development use

Set `DB_TYPE` environment variable to switch between them.
