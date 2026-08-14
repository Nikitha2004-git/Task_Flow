from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.schemas import Priority
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("")
def list_tasks(
    priority: Optional[Priority] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    priority_value = priority.value if priority else None
    return task_service.list_tasks(db, priority=priority_value, search=search)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, payload)


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, payload)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def replace_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)


@router.patch("/{task_id}/move", response_model=schemas.TaskOut)
def move_task(task_id: int, payload: schemas.TaskMove, db: Session = Depends(get_db)):
    return task_service.move_task(db, task_id, payload)
