const PRIORITY_CLASS = {
  Low: "priority-low",
  Medium: "priority-medium",
  High: "priority-high",
};

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString();
}

export default function TaskCard({ task, columns, onEdit, onDelete, onMove }) {
  const handleMoveChange = (event) => {
    const newColumnId = Number(event.target.value);
    if (newColumnId !== task.column_id) {
      onMove(task.id, newColumnId);
    }
  };

  const handleDelete = () => {
    if (window.confirm(`Delete "${task.title}"?`)) {
      onDelete(task.id);
    }
  };

  return (
    <div className="task-card">
      <h4 className="task-title">{task.title}</h4>
      {task.description && <p className="task-description">{task.description}</p>}
      <div className="task-meta">
        <span className={`priority-badge ${PRIORITY_CLASS[task.priority]}`}>
          {task.priority}
        </span>
        <span className="task-date">{formatDate(task.created_at)}</span>
      </div>

      <div className="task-actions">
        <button className="btn btn-small" onClick={() => onEdit(task)}>
          Edit
        </button>
        <button className="btn btn-small btn-danger" onClick={handleDelete}>
          Delete
        </button>
      </div>

      <div className="task-move">
        <label htmlFor={`move-${task.id}`}>Move to:</label>
        <select id={`move-${task.id}`} value={task.column_id} onChange={handleMoveChange}>
          {columns.map((column) => (
            <option key={column.id} value={column.id}>
              {column.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
