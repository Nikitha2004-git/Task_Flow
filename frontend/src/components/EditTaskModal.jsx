import { useState } from "react";

export default function EditTaskModal({ task, onSave, onClose }) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [priority, setPriority] = useState(task.priority);
  const [validationError, setValidationError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!title.trim()) {
      setValidationError("Title is required.");
      return;
    }

    setValidationError("");
    onSave(task.id, {
      title: title.trim(),
      description: description.trim() || null,
      priority,
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(event) => event.stopPropagation()}>
        <form onSubmit={handleSubmit}>
          <h3>Edit Task</h3>

          <label htmlFor="edit-title">Title *</label>
          <input
            id="edit-title"
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            autoFocus
          />

          <label htmlFor="edit-description">Description</label>
          <textarea
            id="edit-description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            rows={3}
          />

          <label htmlFor="edit-priority">Priority</label>
          <select
            id="edit-priority"
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>

          {validationError && <p className="field-error">{validationError}</p>}

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
