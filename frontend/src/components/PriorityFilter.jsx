const PRIORITIES = ["All", "Low", "Medium", "High"];

export default function PriorityFilter({ value, onChange }) {
  return (
    <div className="priority-filter">
      <label htmlFor="priority-filter-select">Priority:</label>
      <select
        id="priority-filter-select"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        {PRIORITIES.map((priority) => (
          <option key={priority} value={priority}>
            {priority}
          </option>
        ))}
      </select>
    </div>
  );
}
