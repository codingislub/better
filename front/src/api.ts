import axios from 'axios';
import type { Task, TaskFormData, DeleteResponse } from './types';

const API_BASE_URL = '/api';

export const taskAPI = {
  getAll: async (): Promise<Task[]> => {
    const response = await axios.get<Task[]>(`${API_BASE_URL}/tasks`);
    return response.data;
  },
  
  getById: async (id: string): Promise<Task> => {
    const response = await axios.get<Task>(`${API_BASE_URL}/tasks/${id}`);
    return response.data;
  },
  
  create: async (taskData: TaskFormData): Promise<Task> => {
    const response = await axios.post<Task>(`${API_BASE_URL}/tasks`, taskData);
    return response.data;
  },
  
  update: async (id: string, taskData: Partial<TaskFormData>): Promise<Task> => {
    const response = await axios.put<Task>(`${API_BASE_URL}/tasks/${id}`, taskData);
    return response.data;
  },
  
  delete: async (id: string): Promise<DeleteResponse> => {
    const response = await axios.delete<DeleteResponse>(`${API_BASE_URL}/tasks/${id}`);
    return response.data;
  }
};
