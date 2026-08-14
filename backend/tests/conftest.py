import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Board, Column, Task

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def db_session():
    # StaticPool is required for an in-memory SQLite DB used across threads:
    # TestClient dispatches requests to a worker thread, and without
    # StaticPool each thread would get its own connection — and therefore
    # its own empty in-memory database — causing "no such table" errors.
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _enable_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded_board(db_session):
    """Seed a board with To Do (2 tasks), In Progress (1 task), Done (1 task)."""
    board = Board(name="Test Board")
    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    todo = Column(board_id=board.id, name="To Do", position=1)
    in_progress = Column(board_id=board.id, name="In Progress", position=2)
    done = Column(board_id=board.id, name="Done", position=3)
    db_session.add_all([todo, in_progress, done])
    db_session.commit()
    db_session.refresh(todo)
    db_session.refresh(in_progress)
    db_session.refresh(done)

    tasks = [
        Task(column_id=todo.id, title="Task A", priority="High"),
        Task(column_id=todo.id, title="Task B", priority="Low"),
        Task(column_id=in_progress.id, title="Task C", priority="Medium"),
        Task(column_id=done.id, title="Task D", priority="Medium"),
    ]
    db_session.add_all(tasks)
    db_session.commit()

    return {
        "board": board,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
        "tasks": tasks,
    }
