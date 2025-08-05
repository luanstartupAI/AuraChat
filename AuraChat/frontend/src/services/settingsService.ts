import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'; // Get from .env

// Function to get the JWT token (replace with your actual auth context/storage)
const getAuthToken = () => {
    return localStorage.getItem('authToken'); // Example: retrieve token from local storage
};

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the token in headers
apiClient.interceptors.request.use(
    (config) => {
        const token = getAuthToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// --- Settings API Calls ---

export const getSettings = async () => {
    try {
        const response = await apiClient.get('/settings/');
        return response.data.settings; // Assuming the API returns { status: 'success', settings: {...} }
    } catch (error) {
        console.error('Error fetching settings:', error);
        throw error;
    }
};

export const getSetting = async (key: string) => {
    try {
        const response = await apiClient.get(`/settings/${key}`);
        return response.data.setting; // Assuming { status: 'success', setting: {...} }
    } catch (error) {
        console.error(`Error fetching setting ${key}:`, error);
        throw error;
    }
};

export const updateSetting = async (key: string, value: string, description: string | null = null) => {
    try {
        const payload = { key, value, description };
        const response = await apiClient.post('/settings/', payload);
        return response.data; // Assuming { status: 'success', message: '...', setting: {...} }
    } catch (error) {
        console.error(`Error updating setting ${key}:`, error);
        throw error;
    }
};

// Add other API service functions here (e.g., for profile, auth, chat, etc.)

