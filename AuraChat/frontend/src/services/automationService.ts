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

// --- Webhook API Calls ---

export const getWebhooks = async () => {
    try {
        const response = await apiClient.get('/automation/webhooks');
        return response.data.webhooks; // Assuming { status: 'success', webhooks: [...] }
    } catch (error) {
        console.error('Error fetching webhooks:', error);
        throw error;
    }
};

interface CreateWebhookPayload {
    url: string;
    event: string; // e.g., "message.received"
    generate_secret?: boolean;
}

export const createWebhook = async (payload: CreateWebhookPayload) => {
    try {
        const response = await apiClient.post('/automation/webhooks', payload);
        return response.data; // Assuming { status: 'success', message: '...', webhook: {...} }
    } catch (error) {
        console.error('Error creating webhook:', error);
        throw error;
    }
};

interface UpdateWebhookPayload {
    url?: string;
    is_active?: boolean;
}

export const updateWebhook = async (webhookId: number, payload: UpdateWebhookPayload) => {
    try {
        const response = await apiClient.put(`/automation/webhooks/${webhookId}`, payload);
        return response.data; // Assuming { status: 'success', message: '...', webhook: {...} }
    } catch (error) {
        console.error(`Error updating webhook ID ${webhookId}:`, error);
        throw error;
    }
};

export const deleteWebhook = async (webhookId: number) => {
    try {
        const response = await apiClient.delete(`/automation/webhooks/${webhookId}`);
        return response.data; // Assuming { status: 'success', message: '...' }
    } catch (error) {
        console.error(`Error deleting webhook ID ${webhookId}:`, error);
        throw error;
    }
};

// --- Automation Rule API Calls (Example Structure) ---
// Add functions here if/when the rule engine endpoints are implemented
// export const getRules = async () => { ... };
// export const createRule = async (payload) => { ... };
// etc.

