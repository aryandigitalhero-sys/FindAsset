import axios from 'axios';

const API_URL = 'http://localhost:8001/api';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeScript = async (script) => {
  const response = await apiClient.post('/analyze-script', { script });
  return response.data;
};

export const generateAssets = async (script) => {
  const response = await apiClient.post('/generate', { script });
  return response.data;
};
