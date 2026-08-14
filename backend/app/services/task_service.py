from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models, queries
from app.dependencies import get_column_or_404, get_task_or_404
from app.schemas import TaskCreate, TaskMove, TaskUpdate


def create_task(db: Session, payload: TaskCreate) -> models.Task:
    # Validates the destination column exists before creating the task.
    get_column_or_404(db, payload.column_id)

    task = models.Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority.value,
        column_id=payload.column_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(
    db: Session, priority: Optional[str] = None, search: Optional[str] = None
) -> List[dict]:
    # Priority/search filtering happens at the database query level.
    if priority is not None:
        return queries.get_tasks_by_priority(db, priority)
    if search is not None:
        return queries.search_tasks_by_title(db, search)
    result = db.execute(
        text(
            "SELECT id, column_id, title, description, priority, created_at "
            "FROM tasks ORDER BY created_at DESC"
        )
    )
    return [dict(row._mapping) for row in result]


def get_task(db: Session, task_id: int) -> models.Task:
    return get_task_or_404(db, task_id)


def update_task(db: Session, task_id: int, payload: TaskUpdate) -> models.Task:
    task = get_task_or_404(db, task_id)

    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.priority is not None:
        task.priority = payload.priority.value

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()


def move_task(db: Session, task_id: int, payload: TaskMove) -> models.Task:
    task = get_task_or_404(db, task_id)
    # Validates the destination column exists before moving.
    get_column_or_404(db, payload.column_id)

    task.column_id = payload.column_id
    db.commit()
    db.refresh(task)
    return task
