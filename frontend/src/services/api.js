import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
});

const DEFAULT_BOARD_ID = 1;

export const api = {
  getBoard: (boardId = DEFAULT_BOARD_ID) =>
    client.get(`/api/boards/${boardId}`).then((res) => res.data),

  createTask: (task) => client.post("/api/tasks", task).then((res) => res.data),

  updateTask: (taskId, updates) =>
    client.patch(`/api/tasks/${taskId}`, updates).then((res) => res.data),

  deleteTask: (taskId) => client.delete(`/api/tasks/${taskId}`),

  moveTask: (taskId, columnId) =>
    client
      .patch(`/api/tasks/${taskId}/move`, { column_id: columnId })
      .then((res) => res.data),

  getTasksByPriority: (priority) =>
    client.get("/api/tasks", { params: { priority } }).then((res) => res.data),
};

export default api;
