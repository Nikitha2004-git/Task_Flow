from app import queries


def test_task_count_per_column(db_session, seeded_board):
    board_id = seeded_board["board"].id

    results = queries.get_task_counts_per_column(db_session, board_id)

    counts = {row["name"]: row["task_count"] for row in results}

    assert counts["To Do"] == 2
    assert counts["In Progress"] == 1
    assert counts["Done"] == 1


def test_task_count_per_column_includes_empty_columns(db_session, seeded_board):
    from app.models import Column

    empty_column = Column(board_id=seeded_board["board"].id, name="Backlog", position=4)
    db_session.add(empty_column)
    db_session.commit()

    results = queries.get_task_counts_per_column(db_session, seeded_board["board"].id)
    counts = {row["name"]: row["task_count"] for row in results}

    assert counts["Backlog"] == 0


def test_get_tasks_by_priority_newest_first(db_session, seeded_board):
    from app.models import Task

    extra = Task(
        column_id=seeded_board["todo"].id, title="Newer high task", priority="High"
    )
    db_session.add(extra)
    db_session.commit()

    results = queries.get_tasks_by_priority(db_session, "High")

    assert len(results) == 2
    # Newest first.
    assert results[0]["title"] == "Newer high task"
