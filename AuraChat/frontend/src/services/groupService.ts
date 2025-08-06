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

// --- Group API Calls ---

export const getGroups = async () => {
    try {
        const response = await apiClient.get('/group/');
        return response.data.groups; // Assuming { status: 'success', groups: [...] }
    } catch (error) {
        console.error('Error fetching groups:', error);
        throw error;
    }
};

export const getGroupDetails = async (groupId: number) => {
    try {
        const response = await apiClient.get(`/group/${groupId}`);
        return response.data.group; // Assuming { status: 'success', group: {...} }
    } catch (error) {
        console.error(`Error fetching group details for ID ${groupId}:`, error);
        throw error;
    }
};

export const createGroup = async (name: string, description: string | null) => {
    try {
        const payload = { name, description };
        const response = await apiClient.post('/group/', payload);
        return response.data; // Assuming { status: 'success', message: '...', group: {...} }
    } catch (error) {
        console.error('Error creating group:', error);
        throw error;
    }
};

export const updateGroup = async (groupId: number, name: string, description: string | null) => {
    try {
        const payload = { name, description };
        const response = await apiClient.put(`/group/${groupId}`, payload);
        return response.data; // Assuming { status: 'success', message: '...', group: {...} }
    } catch (error) {
        console.error(`Error updating group ID ${groupId}:`, error);
        throw error;
    }
};

export const deleteGroup = async (groupId: number) => {
    try {
        const response = await apiClient.delete(`/group/${groupId}`);
        return response.data; // Assuming { status: 'success', message: '...' }
    } catch (error) {
        console.error(`Error deleting group ID ${groupId}:`, error);
        throw error;
    }
};

export const addContactToGroup = async (groupId: number, contactId: number) => {
    try {
        const payload = { contact_id: contactId };
        const response = await apiClient.post(`/group/${groupId}/contacts`, payload);
        return response.data; // Assuming { status: 'success', message: '...' }
    } catch (error) {
        console.error(`Error adding contact ${contactId} to group ${groupId}:`, error);
        throw error;
    }
};

export const removeContactFromGroup = async (groupId: number, contactId: number) => {
    try {
        const response = await apiClient.delete(`/group/${groupId}/contacts/${contactId}`);
        return response.data; // Assuming { status: 'success', message: '...' }
    } catch (error) {
        console.error(`Error removing contact ${contactId} from group ${groupId}:`, error);
        throw error;
    }
};

// --- Contact API Calls (Needed for Group Manager) ---
// Assuming a contact service exists or adding basic fetch here

export const getContacts = async (searchTerm: string = '') => {
    try {
        // Adjust endpoint and params based on your actual contact API
        const response = await apiClient.get(`/contact/contacts?search=${searchTerm}&limit=50`); 
        return response.data.contacts; // Assuming { status: 'success', contacts: [...] } 
    } catch (error) {
        console.error('Error fetching contacts:', error);
        throw error;
    }
};

