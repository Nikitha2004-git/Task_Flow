import TaskCard from "./TaskCard.jsx";

export default function Column({ column, allColumns, onEdit, onDelete, onMove }) {
  return (
    <div className="column">
      <div className="column-header">
        <h3>
          {column.name} ({column.tasks.length})
        </h3>
      </div>

      <div className="column-tasks">
        {column.tasks.length === 0 ? (
          <p className="empty-state">No tasks yet.</p>
        ) : (
          column.tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              columns={allColumns}
              onEdit={onEdit}
              onDelete={onDelete}
              onMove={onMove}
            />
          ))
        )}
      </div>
    </div>
  );
}
