import axios from 'axios';
import { ChatResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export const chatApi = {
  sendMessage: async (message: string): Promise<string> => {
    const formData = new FormData();
    formData.append('message', message);
    
    const response = await api.post('/chat', formData);
    
    // Since your backend redirects to '/', we need to handle this differently
    // We'll need to fetch the updated chat history or modify the backend to return JSON
    return response.data;
  },

  clearChat: async (): Promise<void> => {
    await api.post('/clear_chat');
  },

  toggleDarkMode: async (): Promise<void> => {
    await api.post('/toggle_dark_mode');
  },

  getChatHistory: async (): Promise<any> => {
    const response = await api.get('/');
    return response.data;
  },

  getDashboard: async (): Promise<any> => {
    const response = await api.get('/dashboard');
    return response.data;
  },
};

export default api;