# TaskFlow — Full-Stack Task Board

## Description

TaskFlow is a lightweight Trello-style task board built with React, FastAPI, and SQLite. It lets you create, edit, move, delete, and filter tasks across three columns (To Do, In Progress, Done) on a single demo board. The backend is the source of truth — every change goes through a validated REST API and is persisted to a relational SQLite database.

## Features

**Core features**
- Board view with columns and tasks
- Create task (with required title, optional description/priority/column)
- Edit task (title, description, priority)
- Delete task
- Move task between columns (dropdown-based)
- Priority filtering (All / Low / Medium / High)
- Relational database persistence (boards → columns → tasks, with foreign keys)
- Backend validation (empty/whitespace titles rejected, priority restricted to Low/Medium/High, column existence checked)
- Frontend error handling with user-friendly messages
- Loading and empty states
- Automated backend tests (pytest)

**Stretch feature implemented**
- Task count in column header, e.g. `To Do (2)`

## Tech Stack

**Frontend**
- React
- Vite
- Axios
- Plain CSS

**Backend**
- Python
- FastAPI
- Pydantic
- SQLAlchemy + SQLite

**Testing**
- pytest

## Project Structure

```
taskflow/
  backend/
    app/
      main.py            FastAPI app, CORS, router registration
      database.py         SQLAlchemy engine/session, SQLite FK enforcement
      models.py            ORM models (Board, Column, Task)
      schemas.py           Pydantic request/response schemas + validation
      dependencies.py      Shared 404 lookup helpers
      queries.py           Raw SQL queries (aggregation, filtering, search)
      routes/               API route handlers (boards, columns, tasks)
      services/
        task_service.py    Business logic for task CRUD/move
    tests/                 pytest suite
    schema.sql              Documented CREATE TABLE statements
    seed.py                 Demo data seed script
    requirements.txt
  frontend/
    src/
      components/           Board, Column, TaskCard, TaskForm, EditTaskModal,
                             PriorityFilter, ErrorMessage
      services/api.js       Axios API client
      App.jsx, main.jsx
      styles/app.css
```

## Database Design

```
Board (1) ──< Column (1) ──< Task
```

- `boards`: `id`, `name` (NOT NULL), `created_at`
- `columns`: `id`, `board_id` (FK → boards.id, NOT NULL), `name` (NOT NULL), `position` (NOT NULL), `created_at`
- `tasks`: `id`, `column_id` (FK → columns.id, NOT NULL), `title` (NOT NULL), `description`, `priority` (NOT NULL, CHECK constrained to `Low`/`Medium`/`High`), `created_at`

Foreign keys cascade on delete, and `PRAGMA foreign_keys=ON` is enabled on every SQLite connection (see `app/database.py`). Indexes exist on `columns.board_id`, `tasks.column_id`, and `tasks.priority`. The full DDL lives in `backend/schema.sql`.

## SQL Queries

Both live in `backend/app/queries.py` and run directly against SQLite (no in-Python filtering/aggregation):

**1. Task count per column** — used by `GET /api/boards/{id}/task-counts`
```sql
SELECT c.id, c.name, COUNT(t.id) AS task_count
FROM columns c
LEFT JOIN tasks t ON t.column_id = c.id
WHERE c.board_id = ?
GROUP BY c.id, c.name
ORDER BY c.position;
```

**2. Tasks by priority, newest first** — used by `GET /api/tasks?priority=High`
```sql
SELECT id, column_id, title, description, priority, created_at
FROM tasks
WHERE priority = ?
ORDER BY created_at DESC;
```

## Seed Data

`backend/seed.py` creates one demo board ("TaskFlow Demo Board") with columns To Do / In Progress / Done and four sample tasks across different priorities. It is idempotent — re-running it clears and re-creates the data.

## Installation

```bash
git clone https://github.com/Nikitha2004-git/Task_Flow.git
cd Task_Flow
```

**Backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```
The API runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
The app runs at `http://localhost:5173`.

## Environment Variables

**backend/.env** (copy from `.env.example`)
```
DATABASE_URL=sqlite:///./taskflow.db
FRONTEND_ORIGIN=http://localhost:5173
```

**frontend/.env** (copy from `.env.example`)
```
VITE_API_BASE_URL=http://localhost:8000
```

## Running Tests

```markdown
```bash
cd backend
pytest -v
```

Covers: empty/whitespace title rejection, title stripping, priority validation, task creation/update/delete, move-updates-column (verified against the database), 404s for missing tasks/columns/boards, priority filtering, and the task-count SQL query against known seeded data (To Do=2, In Progress=1, Done=1).

## API Documentation

Key endpoints (full interactive docs at `/docs` once the server is running):

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/boards/{board_id}` | Board with nested columns and tasks |
| GET | `/api/boards/{board_id}/task-counts` | Task count per column (SQL query 1) |
| GET | `/api/tasks?priority=High` | Filter tasks by priority (SQL query 2) |
| GET | `/api/tasks/{task_id}` | Single task, 404 if missing |
| POST | `/api/tasks` | Create task (title required, priority defaults to Medium) |
| PATCH | `/api/tasks/{task_id}` | Update title/description/priority |
| DELETE | `/api/tasks/{task_id}` | Delete task |
| PATCH | `/api/tasks/{task_id}/move` | Move task to another column |

## Assumptions

- The application currently uses one demo board (id=1); the schema supports multiple boards, but the UI doesn't expose board switching.
- Authentication is intentionally excluded — outside the assignment scope.
- Tasks belong to exactly one column and have exactly one priority.
- Default priority is `Medium` when not specified.
- Priority filtering on the board view is applied client-side to the already-fetched nested board data (to preserve column grouping in one request); the dedicated `GET /api/tasks?priority=` endpoint performs the filtering at the database level, as required.

## Improvements With More Time

- Drag-and-drop (kept to dropdown-based move per the assignment's phased approach)
- Text search by task title
- Better accessibility (keyboard navigation, ARIA roles for modals)
- Pagination for large boards
- PostgreSQL for production instead of SQLite
- More comprehensive test coverage (frontend tests, edge cases)
- Docker Compose for one-command local setup
- CI/CD pipeline

## Deployment Notes

Recommended: frontend on Vercel, backend on Render/Railway/Fly.io. SQLite persistence is **not guaranteed** on ephemeral hosting — use a host with a persistent disk, or switch to PostgreSQL for production while keeping SQLite for local development. The frontend must not hard-code `http://localhost:8000`; set `VITE_API_BASE_URL` to the deployed backend URL, and set `FRONTEND_ORIGIN` on the backend to the deployed frontend URL.

## Time Spent

Approximately 5-6 hours across design, backend, frontend, and testing.

## Learning

Writing the task-count query as a `LEFT JOIN` with `GROUP BY` at the database level (rather than fetching all tasks and counting them in Python) reinforced why relational aggregation belongs in SQL — it's simpler, faster, and scales independently of application memory.

## Testing Status

The backend test suite has been run locally with pytest.

```text
17 passed, 124 warnings in 0.53s
```

The 17 tests cover task creation and validation, task updates and deletion, moving tasks between columns, priority filtering, missing-resource handling, board retrieval, and database-level task-count and priority queries.

The warnings are SQLAlchemy deprecation warnings related to `datetime.utcnow()` and do not affect the test results.