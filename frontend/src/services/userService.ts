import apiClient, { handleApiResponse, handleApiError } from './api';

// User types
export interface UserProfile {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  bio?: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProfileUpdate {
  full_name?: string;
  bio?: string;
  avatar_url?: string;
}

export interface UserPreferences {
  style_preference?: string;
  color_preference?: string;
  body_type?: string;
  budget_range?: string;
  preferred_brands?: string[];
  size_info?: {
    top_size?: string;
    bottom_size?: string;
    shoe_size?: string;
  };
}

export interface UserListResponse {
  users: UserProfile[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

class UserService {
  // Get current user profile
  async getProfile(): Promise<UserProfile> {
    try {
      const response = await apiClient.get('/users/me');
      return handleApiResponse<UserProfile>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Update user profile
  async updateProfile(updateData: UserProfileUpdate): Promise<UserProfile> {
    try {
      const response = await apiClient.put('/users/me', updateData);
      return handleApiResponse<UserProfile>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get user preferences
  async getPreferences(): Promise<UserPreferences> {
    try {
      const response = await apiClient.get('/users/me/preferences');
      return handleApiResponse<UserPreferences>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Update user preferences
  async updatePreferences(preferences: UserPreferences): Promise<UserPreferences> {
    try {
      const response = await apiClient.put('/users/me/preferences', preferences);
      return handleApiResponse<UserPreferences>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Upload avatar
  async uploadAvatar(file: File): Promise<{ avatar_url: string }> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post('/users/me/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return handleApiResponse<{ avatar_url: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Delete user account
  async deleteAccount(): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete('/users/me');
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get user by ID (admin function)
  async getUserById(userId: string): Promise<UserProfile> {
    try {
      const response = await apiClient.get(`/users/${userId}`);
      return handleApiResponse<UserProfile>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // List users (admin function)
  async listUsers(
    page: number = 1,
    size: number = 20,
    statusFilter?: string
  ): Promise<UserListResponse> {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
      });

      if (statusFilter) {
        params.append('status_filter', statusFilter);
      }

      const response = await apiClient.get(`/users?${params.toString()}`);
      return handleApiResponse<UserListResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Update user status (admin function)
  async updateUserStatus(
    userId: string,
    status: string
  ): Promise<{ message: string }> {
    try {
      const response = await apiClient.patch(`/users/${userId}/status`, {
        status,
      });
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }
}

// Export singleton instance
export const userService = new UserService();
export default userService;