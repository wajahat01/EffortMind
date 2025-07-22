import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;

export async function postPrediction(formData) {
  try {
    const response = await api.post('/predict', formData);
    return response.data;
  } catch (error) {
    throw error;
  }
} 