from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column as SAColumn,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = SAColumn(Integer, primary_key=True, autoincrement=True)
    name = SAColumn(String, nullable=False)
    created_at = SAColumn(DateTime, nullable=False, default=datetime.utcnow)

    columns = relationship(
        "Column",
        back_populates="board",
        cascade="all, delete-orphan",
        order_by="Column.position",
    )


class Column(Base):
    __tablename__ = "columns"

    id = SAColumn(Integer, primary_key=True, autoincrement=True)
    board_id = SAColumn(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    name = SAColumn(String, nullable=False)
    position = SAColumn(Integer, nullable=False)
    created_at = SAColumn(DateTime, nullable=False, default=datetime.utcnow)

    board = relationship("Board", back_populates="columns")
    tasks = relationship(
        "Task",
        back_populates="column",
        cascade="all, delete-orphan",
        order_by="Task.created_at",
    )


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("priority IN ('Low', 'Medium', 'High')", name="ck_task_priority"),
    )

    id = SAColumn(Integer, primary_key=True, autoincrement=True)
    column_id = SAColumn(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    title = SAColumn(String, nullable=False)
    description = SAColumn(Text, nullable=True)
    priority = SAColumn(String, nullable=False, default="Medium")
    created_at = SAColumn(DateTime, nullable=False, default=datetime.utcnow)

    column = relationship("Column", back_populates="tasks")
