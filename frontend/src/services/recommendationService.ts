import apiClient, { handleApiResponse, handleApiError } from './api';

// Recommendation types
export interface OutfitRecommendation {
  id: string;
  title: string;
  description: string;
  image_url: string;
  items: RecommendationItem[];
  style_tags: string[];
  occasion: string[];
  price_range: {
    min: number;
    max: number;
    currency: string;
  };
  confidence_score: number;
  trend_score: number;
  social_stats: {
    likes: number;
    shares: number;
    saves: number;
  };
  created_at: string;
}

export interface RecommendationItem {
  id: string;
  name: string;
  category: string;
  brand?: string;
  price: number;
  currency: string;
  image_url: string;
  product_url?: string;
  color: string;
  size_available: string[];
  material?: string;
  sustainability_score?: number;
}

export interface RecommendationRequest {
  user_context?: {
    occasion?: string;
    style_preference?: string;
    body_type?: string;
    color_preference?: string;
    budget_min?: number;
    budget_max?: number;
    size_info?: {
      top_size?: string;
      bottom_size?: string;
      shoe_size?: string;
    };
  };
  image_context?: {
    image_url: string;
    analysis_id?: string;
  };
  filters?: {
    categories?: string[];
    brands?: string[];
    price_range?: {
      min: number;
      max: number;
    };
    colors?: string[];
    occasions?: string[];
    sustainability_min_score?: number;
  };
  limit?: number;
}

export interface TrendingRecommendation {
  id: string;
  title: string;
  description: string;
  image_url: string;
  trend_type: 'seasonal' | 'celebrity' | 'social' | 'runway';
  popularity_score: number;
  time_period: string;
  related_items: RecommendationItem[];
  hashtags: string[];
}

export interface PersonalizedFeed {
  recommendations: OutfitRecommendation[];
  trending: TrendingRecommendation[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface SimilarOutfitsRequest {
  reference_image_url: string;
  similarity_threshold?: number;
  include_price_range?: boolean;
  max_results?: number;
}

export interface RecommendationFeedback {
  recommendation_id: string;
  feedback_type: 'like' | 'dislike' | 'save' | 'share' | 'purchase';
  rating?: number; // 1-5 scale
  comments?: string;
}

class RecommendationService {
  // Get personalized recommendations
  async getRecommendations(request: RecommendationRequest): Promise<OutfitRecommendation[]> {
    try {
      const response = await apiClient.post('/recommendations', request);
      return handleApiResponse<OutfitRecommendation[]>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get personalized feed
  async getPersonalizedFeed(
    page: number = 1,
    size: number = 20,
    filters?: RecommendationRequest['filters']
  ): Promise<PersonalizedFeed> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      const requestBody = filters ? { filters } : {};

      const response = await apiClient.post(`/recommendations/feed?${params.toString()}`, requestBody);
      return handleApiResponse<PersonalizedFeed>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get trending recommendations
  async getTrendingRecommendations(
    trend_type?: string,
    limit: number = 10
  ): Promise<TrendingRecommendation[]> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
      });

      if (trend_type) {
        params.append('trend_type', trend_type);
      }

      const response = await apiClient.get(`/recommendations/trending?${params.toString()}`);
      return handleApiResponse<TrendingRecommendation[]>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get similar outfits
  async getSimilarOutfits(request: SimilarOutfitsRequest): Promise<OutfitRecommendation[]> {
    try {
      const response = await apiClient.post('/recommendations/similar', request);
      return handleApiResponse<OutfitRecommendation[]>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get recommendation by ID
  async getRecommendationById(recommendationId: string): Promise<OutfitRecommendation> {
    try {
      const response = await apiClient.get(`/recommendations/${recommendationId}`);
      return handleApiResponse<OutfitRecommendation>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Submit feedback for recommendation
  async submitFeedback(feedback: RecommendationFeedback): Promise<{ message: string }> {
    try {
      const response = await apiClient.post('/recommendations/feedback', feedback);
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get user's saved recommendations
  async getSavedRecommendations(
    page: number = 1,
    size: number = 20
  ): Promise<{
    recommendations: OutfitRecommendation[];
    total: number;
    page: number;
    size: number;
    pages: number;
  }> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      const response = await apiClient.get(`/recommendations/saved?${params.toString()}`);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Save/unsave recommendation
  async toggleSaveRecommendation(
    recommendationId: string,
    save: boolean = true
  ): Promise<{ message: string }> {
    try {
      const endpoint = save ? 'save' : 'unsave';
      const response = await apiClient.post(`/recommendations/${recommendationId}/${endpoint}`);
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get recommendation history
  async getRecommendationHistory(
    page: number = 1,
    size: number = 20
  ): Promise<{
    recommendations: OutfitRecommendation[];
    total: number;
    page: number;
    size: number;
    pages: number;
  }> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      const response = await apiClient.get(`/recommendations/history?${params.toString()}`);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Search recommendations
  async searchRecommendations(
    query: string,
    filters?: RecommendationRequest['filters'],
    page: number = 1,
    size: number = 20
  ): Promise<{
    recommendations: OutfitRecommendation[];
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

      const requestBody = filters ? { filters } : {};

      const response = await apiClient.post(`/recommendations/search?${params.toString()}`, requestBody);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get seasonal recommendations
  async getSeasonalRecommendations(
    season?: 'spring' | 'summer' | 'fall' | 'winter',
    limit: number = 20
  ): Promise<OutfitRecommendation[]> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
      });

      if (season) {
        params.append('season', season);
      }

      const response = await apiClient.get(`/recommendations/seasonal?${params.toString()}`);
      return handleApiResponse<OutfitRecommendation[]>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get occasion-based recommendations
  async getOccasionRecommendations(
    occasion: string,
    limit: number = 20
  ): Promise<OutfitRecommendation[]> {
    try {
      const params = new URLSearchParams({
        occasion,
        limit: limit.toString(),
      });

      const response = await apiClient.get(`/recommendations/occasion?${params.toString()}`);
      return handleApiResponse<OutfitRecommendation[]>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }
}

// Export singleton instance
export const recommendationService = new RecommendationService();
export default recommendationService;