import { useState } from "react";

export default function TaskForm({ columns, onSubmit, onCancel }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("Medium");
  const [columnId, setColumnId] = useState(columns[0]?.id ?? "");
  const [validationError, setValidationError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!title.trim()) {
      setValidationError("Title is required.");
      return;
    }

    setValidationError("");
    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      column_id: Number(columnId),
    });
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <h3>Add Task</h3>

      <label htmlFor="task-title">Title *</label>
      <input
        id="task-title"
        type="text"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        autoFocus
      />

      <label htmlFor="task-description">Description</label>
      <textarea
        id="task-description"
        value={description}
        onChange={(event) => setDescription(event.target.value)}
        rows={3}
      />

      <label htmlFor="task-priority">Priority</label>
      <select
        id="task-priority"
        value={priority}
        onChange={(event) => setPriority(event.target.value)}
      >
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>

      <label htmlFor="task-column">Column</label>
      <select
        id="task-column"
        value={columnId}
        onChange={(event) => setColumnId(event.target.value)}
      >
        {columns.map((column) => (
          <option key={column.id} value={column.id}>
            {column.name}
          </option>
        ))}
      </select>

      {validationError && <p className="field-error">{validationError}</p>}

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          Create Task
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}
