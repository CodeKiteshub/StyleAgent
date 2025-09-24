// Export all services for easy importing
export { default as apiClient } from './api';
export { authService } from './authService';
export { userService } from './userService';
export { chatService } from './chatService';
export { imageService } from './imageService';
export { recommendationService } from './recommendationService';

// Export types
export type {
  ApiResponse,
  ApiError,
} from './api';

export type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
} from './authService';

export type {
  UserProfile,
  UserProfileUpdate,
  UserPreferences,
  UserListResponse,
} from './userService';

export type {
  ChatMessage,
  Conversation,
  CreateConversationRequest,
  SendMessageRequest,
  ChatResponse,
  ConversationListResponse,
} from './chatService';

export type {
  ImageAnalysisResult,
  ClothingItem,
  ColorAnalysis,
  ImageUploadResponse,
  OutfitAnalysisRequest,
  StyleTransferRequest,
  StyleTransferResult,
} from './imageService';

export type {
  OutfitRecommendation,
  RecommendationItem,
  RecommendationRequest,
  TrendingRecommendation,
  PersonalizedFeed,
  SimilarOutfitsRequest,
  RecommendationFeedback,
} from './recommendationService';