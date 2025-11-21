# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based todo list application with a layered architecture:
- **Controller**: Flask routes and HTTP handlers (controller layer)
- **Logic**: Business logic for processing todos (service layer)
- **Repository**: Database interactions using SQLAlchemy (data access layer)

The application connects to a PostgreSQL database for persistence.

## Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database (configured via environment variables or hardcoded in repository)
- Virtual environment activated

### Installation
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
pip install Flask SQLAlchemy psycopg2-binary
```

### Running the Application
```bash
python main.py
```
The Flask application runs on `http://0.0.0.0:8574` by default.

### Checking Application Health
```bash
curl http://localhost:8574/health
```
Should return "OK" with 200 status.

## Architecture

### Layered Architecture Pattern
The codebase follows a three-layer architecture:

1. **Controller Layer** (`controller/todos_controller.py`)
   - Handles HTTP requests and responses
   - Routes are registered in the `setup_routes()` method
   - Delegates business logic to the logic layer

2. **Logic Layer** (`logic/todos_logic.py`)
   - Contains business logic for todo operations
   - Currently empty but intended for service methods

3. **Repository Layer** (`repository/postgres_repository.py`)
   - Manages database interactions using SQLAlchemy ORM
   - Defines database models: `Users` and `Todos`
   - Uses scoped sessions for thread-safe database access

### Database Configuration
Located in `repository/postgres_repository.py`:
- **Connection String**: `postgresql://postgres:12345@postgres:5432/todos-db`
- **Credentials**: Username is `postgres`, password is `12345` (hardcoded - should use environment variables in production)
- **Database**: `todos-db`

### Key Dependencies
- **Flask 3.1.1**: Web framework for HTTP endpoints
- **SQLAlchemy 2.0.44**: ORM for database interactions
- **PostgreSQL**: Database backend

## Key Files and Responsibilities

| File | Responsibility |
|------|-----------------|
| `main.py` | Application entry point, Flask app initialization |
| `controller/todos_controller.py` | HTTP route handlers |
| `logic/todos_logic.py` | Business logic (placeholder) |
| `repository/postgres_repository.py` | ORM models and database configuration |
| `controller/__init__.py` | Controller package marker |

## Common Development Tasks

### Adding a New Endpoint
1. Create the route handler in `TodosController.setup_routes()` method
2. Implement business logic in `logic/todos_logic.py`
3. Use repository models (`Users`, `Todos`) for database operations

### Working with Database Models
- Access `Users` model for user-related data
- Access `Todos` model for todo items
- Use `Session` from repository module for database transactions
- Models are defined using SQLAlchemy declarative syntax in `repository/postgres_repository.py`

### Database Migrations
Database models are defined in the ORM but tables should be created with:
```python
from repository.postgres_repository import Base, engine
Base.metadata.create_all(engine)
```

## Current Status

- Basic Flask application structure is in place
- Health check endpoint (`/health`) is implemented
- Database models are defined but business logic is incomplete
- The `/register` endpoint is partially stubbed out in the controller