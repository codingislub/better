import React from 'react';
import './Header.css';

interface HeaderProps {
  onNewTask: () => void;
}

const Header: React.FC<HeaderProps> = ({ onNewTask }) => {
  return (
    <div className="header">
      <div className="header-content">
        <div>
          <h1>✨ Task Manager</h1>
          <p>Organize your life, one task at a time 🚀</p>
        </div>
        <button className="new-task-btn" onClick={onNewTask}>
          <span>➕ New Task</span>
        </button>
      </div>
    </div>
  );
};

export default Header;
