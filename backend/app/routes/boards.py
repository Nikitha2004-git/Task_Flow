from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import queries, schemas
from app.database import get_db
from app.dependencies import get_board_or_404

router = APIRouter(prefix="/api/boards", tags=["boards"])


@router.get("/{board_id}", response_model=schemas.BoardOut)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = get_board_or_404(db, board_id)
    return board


@router.get("/{board_id}/task-counts", response_model=List[schemas.TaskCountOut])
def get_task_counts(board_id: int, db: Session = Depends(get_db)):
    get_board_or_404(db, board_id)
    return queries.get_task_counts_per_column(db, board_id)
