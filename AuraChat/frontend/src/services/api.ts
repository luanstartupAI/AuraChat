const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('aura_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: this.getAuthHeaders(),
      ...options
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Auth endpoints
  async login(email: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  }

  async register(name: string, email: string, password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    });
  }

  async getProfile() {
    return this.request('/auth/me');
  }

  async updateProfile(data: any) {
    return this.request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async changePassword(currentPassword: string, newPassword: string) {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    });
  }

  // Chat endpoints
  async getConversations() {
    return this.request('/chat/conversations');
  }

  async getMessages(chatId: string) {
    return this.request(`/chat/conversations/${chatId}/messages`);
  }

  async sendMessage(chatId: string, content: string, messageType = 'text', mediaUrl?: string) {
    return this.request(`/chat/conversations/${chatId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ content, message_type: messageType, media_url: mediaUrl })
    });
  }

  async markAsRead(chatId: string) {
    return this.request(`/chat/conversations/${chatId}/read`, {
      method: 'POST'
    });
  }

  async getChatStats() {
    return this.request('/chat/stats');
  }

  // Contact endpoints
  async getContacts(page = 1, limit = 20, search = '') {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
      ...(search && { search })
    });
    return this.request(`/contact/contacts?${params}`);
  }

  async getContact(contactId: string) {
    return this.request(`/contact/contacts/${contactId}`);
  }

  async createContact(data: {
    name: string;
    phone: string;
    email?: string;
    tags?: string[];
    notes?: string;
  }) {
    return this.request('/contact/contacts', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateContact(contactId: string, data: any) {
    return this.request(`/contact/contacts/${contactId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async deleteContact(contactId: string) {
    return this.request(`/contact/contacts/${contactId}`, {
      method: 'DELETE'
    });
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }
}

export const apiService = new ApiService();
export default apiService;