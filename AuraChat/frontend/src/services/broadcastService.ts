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

// --- Broadcast Campaign API Calls ---

export const getCampaigns = async () => {
    try {
        const response = await apiClient.get('/broadcast/campaigns');
        return response.data.campaigns; // Assuming { status: 'success', campaigns: [...] }
    } catch (error) {
        console.error('Error fetching campaigns:', error);
        throw error;
    }
};

export const getCampaignDetails = async (campaignId: number) => {
    try {
        const response = await apiClient.get(`/broadcast/campaigns/${campaignId}`);
        return response.data.campaign; // Assuming { status: 'success', campaign: {...} }
    } catch (error) {
        console.error(`Error fetching campaign details for ID ${campaignId}:`, error);
        throw error;
    }
};

interface CreateCampaignPayload {
    name: string;
    message_content: string;
    target_group_id: number;
    scheduled_at?: string | null; // ISO 8601 format string or null/undefined
}

export const createCampaign = async (payload: CreateCampaignPayload) => {
    try {
        const response = await apiClient.post('/broadcast/campaigns', payload);
        return response.data; // Assuming { status: 'success', message: '...', campaign: {...} }
    } catch (error) {
        console.error('Error creating campaign:', error);
        throw error;
    }
};

interface UpdateCampaignPayload {
    name?: string;
    message_content?: string;
    target_group_id?: number;
    scheduled_at?: string | null;
}

export const updateCampaign = async (campaignId: number, payload: UpdateCampaignPayload) => {
    try {
        const response = await apiClient.put(`/broadcast/campaigns/${campaignId}`, payload);
        return response.data; // Assuming { status: 'success', message: '...', campaign: {...} }
    } catch (error) {
        console.error(`Error updating campaign ID ${campaignId}:`, error);
        throw error;
    }
};

export const cancelCampaign = async (campaignId: number) => {
    try {
        const response = await apiClient.post(`/broadcast/campaigns/${campaignId}/cancel`);
        return response.data; // Assuming { status: 'success', message: '...', campaign: {...} }
    } catch (error) {
        console.error(`Error cancelling campaign ID ${campaignId}:`, error);
        throw error;
    }
};

// Note: Delete campaign endpoint might not be implemented based on backend comments.
// export const deleteCampaign = async (campaignId: number) => { ... };

