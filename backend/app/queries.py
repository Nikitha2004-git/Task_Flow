"""Hand-written SQL queries that run directly against SQLite.

These intentionally avoid loading all rows into Python and filtering/
aggregating in application code — the database does that work.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_task_counts_per_column(db: Session, board_id: int):
    """Query 1: task count per column for a given board."""
    sql = text(
        """
        SELECT
            c.id,
            c.name,
            COUNT(t.id) AS task_count
        FROM columns c
        LEFT JOIN tasks t
            ON t.column_id = c.id
        WHERE c.board_id = :board_id
        GROUP BY c.id, c.name
        ORDER BY c.position
        """
    )
    result = db.execute(sql, {"board_id": board_id})
    return [dict(row._mapping) for row in result]


def get_tasks_by_priority(db: Session, priority: str):
    """Query 2: tasks filtered by priority, newest first."""
    sql = text(
        """
        SELECT
            id,
            column_id,
            title,
            description,
            priority,
            created_at
        FROM tasks
        WHERE priority = :priority
        ORDER BY created_at DESC
        """
    )
    result = db.execute(sql, {"priority": priority})
    return [dict(row._mapping) for row in result]


def search_tasks_by_title(db: Session, search_term: str):
    """Optional: database-level title search (used by GET /api/tasks?search=)."""
    sql = text(
        """
        SELECT
            id,
            column_id,
            title,
            description,
            priority,
            created_at
        FROM tasks
        WHERE title LIKE :pattern
        ORDER BY created_at DESC
        """
    )
    result = db.execute(sql, {"pattern": f"%{search_term}%"})
    return [dict(row._mapping) for row in result]
