import React from 'react';
import './TaskList.css';
import type { Task } from '../types';

interface TaskListProps {
  tasks: Task[];
  onTaskClick: (task: Task) => void;
  onEditClick: (task: Task) => void;
  onDeleteClick: (id: string) => void;
  selectedTaskId?: string;
}

const TaskList: React.FC<TaskListProps> = ({ 
  tasks, 
  onTaskClick, 
  onEditClick, 
  onDeleteClick, 
  selectedTaskId 
}) => {
  if (tasks.length === 0) {
    return (
      <div className="empty-list">
        <p>No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map(task => (
        <div
          key={task.id}
          className={`task-item ${selectedTaskId === task.id ? 'selected' : ''}`}
          onClick={() => onTaskClick(task)}
        >
          <div className="task-content">
            <h3>{task.title}</h3>
            {task.description && (
              <p className="task-description">{task.description}</p>
            )}
            <div className="task-meta">
              <span className="task-date">
                {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          <div className="task-actions">
            <button
              className="btn-icon"
              onClick={(e) => {
                e.stopPropagation();
                onEditClick(task);
              }}
              title="Edit task"
            >
              ✏️
            </button>
            <button
              className="btn-icon"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteClick(task.id);
              }}
              title="Delete task"
            >
              🗑️
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
