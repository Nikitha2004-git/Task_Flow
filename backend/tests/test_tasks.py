def test_create_task_with_empty_title_fails(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={"title": "", "column_id": seeded_board["todo"].id},
    )
    assert response.status_code == 400


def test_create_task_with_whitespace_title_fails(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={"title": "   ", "column_id": seeded_board["todo"].id},
    )
    assert response.status_code == 400


def test_create_task_success_defaults_priority_to_medium(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={"title": "New Task", "column_id": seeded_board["todo"].id},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["priority"] == "Medium"
    assert body["title"] == "New Task"


def test_create_task_strips_title_whitespace(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={"title": "  Fix API  ", "column_id": seeded_board["todo"].id},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Fix API"


def test_create_task_invalid_priority_rejected(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Bad priority",
            "column_id": seeded_board["todo"].id,
            "priority": "Urgent",
        },
    )
    assert response.status_code in (400, 422)


def test_create_task_nonexistent_column_returns_404(client, seeded_board):
    response = client.post(
        "/api/tasks",
        json={"title": "Orphan task", "column_id": 9999},
    )
    assert response.status_code == 404


def test_move_task_updates_column(client, seeded_board):
    task = seeded_board["tasks"][0]
    done_column = seeded_board["done"]

    response = client.patch(
        f"/api/tasks/{task.id}/move",
        json={"column_id": done_column.id},
    )
    assert response.status_code == 200
    assert response.json()["column_id"] == done_column.id

    # Verify directly against the database.
    get_response = client.get(f"/api/tasks/{task.id}")
    assert get_response.json()["column_id"] == done_column.id


def test_move_task_to_nonexistent_column_returns_404(client, seeded_board):
    task = seeded_board["tasks"][0]
    response = client.patch(f"/api/tasks/{task.id}/move", json={"column_id": 9999})
    assert response.status_code == 404


def test_get_nonexistent_task_returns_404(client):
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404


def test_delete_task_removes_it(client, seeded_board):
    task = seeded_board["tasks"][0]
    delete_response = client.delete(f"/api/tasks/{task.id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/tasks/{task.id}")
    assert get_response.status_code == 404


def test_update_task_fields(client, seeded_board):
    task = seeded_board["tasks"][0]
    response = client.patch(
        f"/api/tasks/{task.id}",
        json={"title": "Updated title", "priority": "Low"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated title"
    assert body["priority"] == "Low"


def test_filter_tasks_by_priority(client, seeded_board):
    response = client.get("/api/tasks", params={"priority": "Medium"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(t["priority"] == "Medium" for t in body)


def test_get_board_returns_columns_and_tasks(client, seeded_board):
    board_id = seeded_board["board"].id
    response = client.get(f"/api/boards/{board_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Test Board"
    assert len(body["columns"]) == 3
    todo_column = next(c for c in body["columns"] if c["name"] == "To Do")
    assert len(todo_column["tasks"]) == 2


def test_get_nonexistent_board_returns_404(client):
    response = client.get("/api/boards/9999")
    assert response.status_code == 404
