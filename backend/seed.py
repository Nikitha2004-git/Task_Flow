"""Populate the database with a demo board, columns, and sample tasks.

Run with: python seed.py
Safe to re-run — it clears existing data first.
"""

from app.database import Base, SessionLocal, engine
from app.models import Board, Column, Task


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing data so the script is idempotent.
        db.query(Task).delete()
        db.query(Column).delete()
        db.query(Board).delete()
        db.commit()

        board = Board(name="TaskFlow Demo Board")
        db.add(board)
        db.commit()
        db.refresh(board)

        todo = Column(board_id=board.id, name="To Do", position=1)
        in_progress = Column(board_id=board.id, name="In Progress", position=2)
        done = Column(board_id=board.id, name="Done", position=3)
        db.add_all([todo, in_progress, done])
        db.commit()
        db.refresh(todo)
        db.refresh(in_progress)
        db.refresh(done)

        tasks = [
            Task(
                column_id=todo.id,
                title="Create API",
                description="Build the FastAPI backend endpoints",
                priority="High",
            ),
            Task(
                column_id=todo.id,
                title="Design database",
                description="Design the boards/columns/tasks schema",
                priority="Medium",
            ),
            Task(
                column_id=in_progress.id,
                title="Build React UI",
                description="Build the board, columns, and task cards",
                priority="Medium",
            ),
            Task(
                column_id=done.id,
                title="Setup project",
                description="Initialize repo, tooling, and dependencies",
                priority="Low",
            ),
        ]
        db.add_all(tasks)
        db.commit()

        print("Database seeded successfully.")
        print(f"Board: {board.name} (id={board.id})")
        print(f"Columns: {todo.name}, {in_progress.name}, {done.name}")
        print(f"Tasks created: {len(tasks)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
