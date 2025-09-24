import apiClient, { handleApiResponse, handleApiError } from './api';

// Chat types
export interface ChatMessage {
  id: string;
  conversation_id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  metadata?: {
    image_url?: string;
    context?: any;
  };
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message?: string;
}

export interface CreateConversationRequest {
  title?: string;
  initial_message?: string;
}

export interface SendMessageRequest {
  content: string;
  context?: {
    occasion?: string;
    style_preference?: string;
    body_type?: string;
    color_preference?: string;
    budget?: string;
    image_url?: string;
  };
}

export interface ChatResponse {
  message: ChatMessage;
  suggestions?: string[];
  context_updated?: boolean;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

class ChatService {
  // Create new conversation
  async createConversation(data: CreateConversationRequest = {}): Promise<Conversation> {
    try {
      const response = await apiClient.post('/chat/conversations', data);
      return handleApiResponse<Conversation>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get user's conversations
  async getConversations(
    page: number = 1,
    size: number = 20
  ): Promise<ConversationListResponse> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      const response = await apiClient.get(`/chat/conversations?${params.toString()}`);
      return handleApiResponse<ConversationListResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get conversation by ID
  async getConversation(conversationId: string): Promise<Conversation> {
    try {
      const response = await apiClient.get(`/chat/conversations/${conversationId}`);
      return handleApiResponse<Conversation>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get messages for a conversation
  async getMessages(
    conversationId: string,
    page: number = 1,
    size: number = 50
  ): Promise<{ messages: ChatMessage[]; total: number; page: number; size: number; pages: number }> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      const response = await apiClient.get(
        `/chat/conversations/${conversationId}/messages?${params.toString()}`
      );
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Send message to conversation
  async sendMessage(
    conversationId: string,
    messageData: SendMessageRequest
  ): Promise<ChatResponse> {
    try {
      const response = await apiClient.post(
        `/chat/conversations/${conversationId}/messages`,
        messageData
      );
      return handleApiResponse<ChatResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Update conversation title
  async updateConversationTitle(
    conversationId: string,
    title: string
  ): Promise<Conversation> {
    try {
      const response = await apiClient.patch(`/chat/conversations/${conversationId}`, {
        title,
      });
      return handleApiResponse<Conversation>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Delete conversation
  async deleteConversation(conversationId: string): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete(`/chat/conversations/${conversationId}`);
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Delete specific message
  async deleteMessage(
    conversationId: string,
    messageId: string
  ): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete(
        `/chat/conversations/${conversationId}/messages/${messageId}`
      );
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get chat suggestions based on context
  async getChatSuggestions(context?: any): Promise<{ suggestions: string[] }> {
    try {
      const response = await apiClient.post('/chat/suggestions', { context });
      return handleApiResponse<{ suggestions: string[] }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Search messages across conversations
  async searchMessages(
    query: string,
    page: number = 1,
    size: number = 20
  ): Promise<{
    messages: ChatMessage[];
    total: number;
    page: number;
    size: number;
    pages: number;
  }> {
    try {
      const params = new URLSearchParams({
        q: query,
        page: page.toString(),
        size: size.toString(),
      });

      const response = await apiClient.get(`/chat/search?${params.toString()}`);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }
}

// Export singleton instance
export const chatService = new ChatService();
export default chatService;