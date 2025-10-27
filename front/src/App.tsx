import { useState, useEffect } from 'react';
import type { Task, TaskFormData } from './types';
import { taskAPI } from './api';
import Header from './components/Header';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import TaskDetail from './components/TaskDetail';
import './App.css';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const fetchedTasks = await taskAPI.getAll();
      setTasks(fetchedTasks);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks. Make sure the backend is running.');
      console.error('Error fetching tasks:', err);
    }
  };

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task);
    setShowDetail(true);
    setShowForm(false);
  };

  const handleNewTask = () => {
    setEditingTask(null);
    setShowForm(true);
    setShowDetail(false);
  };

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
    setShowDetail(false);
  };

  const handleFormSubmit = async (data: TaskFormData) => {
    try {
      if (editingTask) {
        const updatedTask = await taskAPI.update(editingTask.id, data);
        setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
        if (selectedTask?.id === updatedTask.id) {
          setSelectedTask(updatedTask);
        }
      } else {
        const newTask = await taskAPI.create(data);
        setTasks([...tasks, newTask]);
      }
      setShowForm(false);
      setEditingTask(null);
      setError(null);
    } catch (err) {
      setError('Failed to save task');
      console.error('Error saving task:', err);
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleDeleteClick = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.delete(id);
        setTasks(tasks.filter(t => t.id !== id));
        if (selectedTask?.id === id) {
          setSelectedTask(null);
          setShowDetail(false);
        }
        setError(null);
      } catch (err) {
        setError('Failed to delete task');
        console.error('Error deleting task:', err);
      }
    }
  };

  const handleDetailClose = () => {
    setShowDetail(false);
    setSelectedTask(null);
  };

  return (
    <div className="App">
      <Header onNewTask={handleNewTask} />
      
      {error && (
        <div className="error-message" style={{
          padding: '1rem',
          margin: '1rem',
          backgroundColor: '#fee',
          color: '#c00',
          borderRadius: '4px'
        }}>
          {error}
        </div>
      )}
      
      <div className="container">
        <div className="sidebar">
          <TaskList 
            tasks={tasks}
            onTaskClick={handleTaskClick}
            onEditClick={handleEditClick}
            onDeleteClick={handleDeleteClick}
            selectedTaskId={selectedTask?.id}
          />
        </div>
        
        <div className="main-content">
          {showForm && (
            <TaskForm 
              task={editingTask}
              onSubmit={handleFormSubmit}
              onCancel={handleFormCancel}
            />
          )}
          
          {showDetail && selectedTask && (
            <TaskDetail 
              task={selectedTask}
              onClose={handleDetailClose}
            />
          )}
          
          {!showForm && !showDetail && (
            <div className="welcome-message">
              <h2>Welcome to Task Manager</h2>
              <p>Select a task from the list or create a new one to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
