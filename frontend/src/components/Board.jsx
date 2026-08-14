import Column from "./Column.jsx";

export default function Board({ board, priorityFilter, onEdit, onDelete, onMove }) {
  const columns = board.columns.map((column) => ({
    ...column,
    tasks:
      priorityFilter === "All"
        ? column.tasks
        : column.tasks.filter((task) => task.priority === priorityFilter),
  }));

  return (
    <div className="board">
      {columns.map((column) => (
        <Column
          key={column.id}
          column={column}
          allColumns={board.columns}
          onEdit={onEdit}
          onDelete={onDelete}
          onMove={onMove}
        />
      ))}
    </div>
  );
}
