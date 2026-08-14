from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_board_or_404(db: Session, board_id: int) -> models.Board:
    board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


def get_column_or_404(db: Session, column_id: int) -> models.Column:
    column = db.query(models.Column).filter(models.Column.id == column_id).first()
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


def get_task_or_404(db: Session, task_id: int) -> models.Task:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
