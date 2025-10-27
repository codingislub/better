// Type definitions for Task Manager application
// Frontend only handles Task CRUD operations

export interface Task {
  id: string;
  title: string;
  description: string;
  created_at: string;
}

export interface TaskFormData {
  title: string;
  description: string;
}

export interface DeleteResponse {
  message: string;
  task?: Task;
}

export interface ErrorResponse {
  error: string;
}
