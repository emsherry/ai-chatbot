import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatQueryRequest {
  query: string;
  conversation_id?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface ChatQueryResponse {
  response: string;
  conversation_id: string;
  sources: string[];
  confidence: number;
  tokens_used: number;
  response_time: number;
}

export interface HealthCheck {
  status: string;
  vectorstore_ready: boolean;
  documents_count: number;
}

export const chatApi = {
  async sendMessage(request: ChatQueryRequest): Promise<ChatQueryResponse> {
    const response = await api.post('/chat/query', request);
    return response.data;
  },

  async healthCheck(): Promise<HealthCheck> {
    const response = await api.get('/chat/health');
    return response.data;
  },
};

export const scrapeApi = {
  async scrapeUrl(url: string, options?: {
    max_depth?: number;
    include_pdfs?: boolean;
    force_refresh?: boolean;
  }) {
    const response = await api.post('/scrape', {
      url,
      ...options,
    });
    return response.data;
  },
};

export default api;
