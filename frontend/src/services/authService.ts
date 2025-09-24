import apiClient, { handleApiResponse, handleApiError } from './api';

// Authentication types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    email: string;
    full_name?: string;
    is_active: boolean;
    created_at: string;
  };
}

export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}

class AuthService {
  // Login user
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const formData = new FormData();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const authData = handleApiResponse<AuthResponse>(response);
      
      // Store token in localStorage
      localStorage.setItem('authToken', authData.access_token);
      localStorage.setItem('user', JSON.stringify(authData.user));
      
      return authData;
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Register new user
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/register', userData);
      const authData = handleApiResponse<AuthResponse>(response);
      
      // Store token in localStorage
      localStorage.setItem('authToken', authData.access_token);
      localStorage.setItem('user', JSON.stringify(authData.user));
      
      return authData;
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Logout user
  logout(): void {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }

  // Get current user from localStorage
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = localStorage.getItem('authToken');
    return !!token;
  }

  // Get auth token
  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  // Verify token with backend
  async verifyToken(): Promise<User> {
    try {
      const response = await apiClient.get('/auth/me');
      const user = handleApiResponse<User>(response);
      
      // Update stored user data
      localStorage.setItem('user', JSON.stringify(user));
      
      return user;
    } catch (error: any) {
      // If token verification fails, logout user
      this.logout();
      throw new Error(handleApiError(error));
    }
  }

  // Refresh token (if your backend supports it)
  async refreshToken(): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/refresh');
      const authData = handleApiResponse<AuthResponse>(response);
      
      // Update stored token
      localStorage.setItem('authToken', authData.access_token);
      
      return authData;
    } catch (error: any) {
      this.logout();
      throw new Error(handleApiError(error));
    }
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService;