from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_board_or_404

router = APIRouter(prefix="/api/boards", tags=["columns"])


@router.get("/{board_id}/columns", response_model=List[schemas.ColumnOut])
def list_columns(board_id: int, db: Session = Depends(get_db)):
    get_board_or_404(db, board_id)
    return (
        db.query(models.Column)
        .filter(models.Column.board_id == board_id)
        .order_by(models.Column.position)
        .all()
    )
