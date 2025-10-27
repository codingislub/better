import React from 'react';
import './TaskDetail.css';
import type { Task } from '../types';

interface TaskDetailProps {
  task: Task;
  onClose: () => void;
}

const TaskDetail: React.FC<TaskDetailProps> = ({ task, onClose }) => {
  return (
    <div className="task-detail">
      <div className="detail-header">
        <h2>{task.title}</h2>
        <button className="btn-icon" onClick={onClose} title="Close">
          ×
        </button>
      </div>

      {task.description && (
        <div className="detail-description">
          <p>{task.description}</p>
        </div>
      )}

      <div className="detail-meta">
        <span>Created: {new Date(task.created_at).toLocaleString()}</span>
      </div>
    </div>
  );
};

export default TaskDetail;
