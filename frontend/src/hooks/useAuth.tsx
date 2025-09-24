import React, { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { authService, type User, type LoginRequest, type RegisterRequest } from '../services';
import { useApi } from './useApi';

// Auth context type
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  error: string | null;
}

// Create auth context
export const AuthContext = createContext<AuthContextType | null>(null);

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Auth hook implementation
export function useAuthState() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loginApi = useApi({
    onSuccess: (authData) => {
      setUser(authData.user);
    },
  });

  const registerApi = useApi({
    onSuccess: (authData) => {
      setUser(authData.user);
    },
  });

  const verifyTokenApi = useApi({
    onSuccess: (userData) => {
      setUser(userData);
    },
    onError: () => {
      setUser(null);
      authService.logout();
    },
  });

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      const token = authService.getToken();
      const storedUser = authService.getCurrentUser();

      if (token && storedUser) {
        // Verify token with backend
        try {
          await verifyTokenApi.execute(() => authService.verifyToken());
        } catch (error) {
          // Token verification failed, user will be logged out by the error handler
        }
      }
      
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    await loginApi.execute(() => authService.login(credentials));
  }, [loginApi]);

  const register = useCallback(async (userData: RegisterRequest) => {
    await registerApi.execute(() => authService.register(userData));
  }, [registerApi]);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    if (authService.isAuthenticated()) {
      await verifyTokenApi.execute(() => authService.verifyToken());
    }
  }, [verifyTokenApi]);

  const isAuthenticated = !!user && authService.isAuthenticated();
  const error = loginApi.error || registerApi.error || verifyTokenApi.error;
  const apiLoading = loginApi.loading || registerApi.loading || verifyTokenApi.loading;

  return {
    user,
    isAuthenticated,
    isLoading: isLoading || apiLoading,
    login,
    register,
    logout,
    refreshUser,
    error,
  };
}

// Auth provider component props
interface AuthProviderProps {
  children: React.ReactNode;
}

// Auth provider component
export function AuthProvider({ children }: AuthProviderProps) {
  const authState = useAuthState();

  return (
    <AuthContext.Provider value={authState}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook for protected routes
export function useRequireAuth() {
  const { isAuthenticated, isLoading } = useAuth();
  
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login page or show login modal
      // This depends on your routing setup
      console.warn('User not authenticated, redirect to login');
    }
  }, [isAuthenticated, isLoading]);

  return { isAuthenticated, isLoading };
}

// Hook for guest-only routes (login, register pages)
export function useGuestOnly() {
  const { isAuthenticated, isLoading } = useAuth();
  
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      // Redirect to dashboard or home page
      console.warn('User already authenticated, redirect to dashboard');
    }
  }, [isAuthenticated, isLoading]);

  return { isAuthenticated, isLoading };
}