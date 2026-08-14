import { useCallback, useEffect, useState } from "react";

import Board from "./components/Board.jsx";
import EditTaskModal from "./components/EditTaskModal.jsx";
import ErrorMessage from "./components/ErrorMessage.jsx";
import PriorityFilter from "./components/PriorityFilter.jsx";
import TaskForm from "./components/TaskForm.jsx";
import { api } from "./services/api.js";

export default function App() {
  const [board, setBoard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("All");
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const loadBoard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getBoard();
      setBoard(data);
    } catch (err) {
      setError("Unable to load the board. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBoard();
  }, [loadBoard]);

  const handleCreateTask = async (taskData) => {
    setActionError("");
    try {
      await api.createTask(taskData);
      setShowTaskForm(false);
      await loadBoard();
    } catch (err) {
      setActionError("Unable to create task. Please try again.");
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    setActionError("");
    try {
      await api.updateTask(taskId, updates);
      setEditingTask(null);
      await loadBoard();
    } catch (err) {
      setActionError("Unable to update task. Please try again.");
    }
  };

  const handleDeleteTask = async (taskId) => {
    setActionError("");
    try {
      await api.deleteTask(taskId);
      await loadBoard();
    } catch (err) {
      setActionError("Unable to delete task.");
    }
  };

  const handleMoveTask = async (taskId, columnId) => {
    setActionError("");
    try {
      await api.moveTask(taskId, columnId);
      await loadBoard();
    } catch (err) {
      setActionError("Unable to move task. Please try again.");
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>TaskFlow</h1>
      </header>

      <div className="toolbar">
        <PriorityFilter value={priorityFilter} onChange={setPriorityFilter} />
        <button className="btn btn-primary" onClick={() => setShowTaskForm(true)}>
          + Add Task
        </button>
      </div>

      <ErrorMessage message={actionError} />

      {loading && <p className="loading-state">Loading board...</p>}
      {!loading && error && <ErrorMessage message={error} />}

      {!loading && !error && board && (
        <Board
          board={board}
          priorityFilter={priorityFilter}
          onEdit={setEditingTask}
          onDelete={handleDeleteTask}
          onMove={handleMoveTask}
        />
      )}

      {showTaskForm && board && (
        <div className="modal-overlay" onClick={() => setShowTaskForm(false)}>
          <div className="modal" onClick={(event) => event.stopPropagation()}>
            <TaskForm
              columns={board.columns}
              onSubmit={handleCreateTask}
              onCancel={() => setShowTaskForm(false)}
            />
          </div>
        </div>
      )}

      {editingTask && (
        <EditTaskModal
          task={editingTask}
          onSave={handleUpdateTask}
          onClose={() => setEditingTask(null)}
        />
      )}
    </div>
  );
}
