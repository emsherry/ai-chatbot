import { useState, useCallback, useEffect } from 'react';
import { chatApi, ChatQueryRequest, ChatQueryResponse } from '../services/api';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
  confidence?: number;
}

export interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string;
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
  loadConversation: (id: string) => Promise<void>;
  health: {
    status: string;
    vectorstoreReady: boolean;
    documentsCount: number;
  } | null;
}

export const useChat = (): UseChatReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string>('');
  const [health, setHealth] = useState<UseChatReturn['health']>(null);

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const healthData = await chatApi.healthCheck();
        setHealth({
          status: healthData.status,
          vectorstoreReady: healthData.vectorstore_ready,
          documentsCount: healthData.documents_count,
        });
      } catch (err) {
        console.error('Health check failed:', err);
        setHealth({
          status: 'unhealthy',
          vectorstoreReady: false,
          documentsCount: 0,
        });
      }
    };

    checkHealth();
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    setIsLoading(true);
    setError(null);

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const request: ChatQueryRequest = {
        query: content.trim(),
        conversation_id: conversationId || undefined,
        max_tokens: 500,
        temperature: 0.7,
      };

      const response: ChatQueryResponse = await chatApi.sendMessage(request);

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        sources: response.sources,
        confidence: response.confidence,
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      
      // Add error message
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId('');
    setError(null);
  }, []);

  const loadConversation = useCallback(async (id: string) => {
    // In a real implementation, this would load a specific conversation
    // For now, we'll just reset and set the conversation ID
    setMessages([]);
    setConversationId(id);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    sendMessage,
    clearMessages,
    loadConversation,
    health,
  };
};
