import { useState, useCallback } from 'react';

// Generic API hook for handling loading states and errors
export interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export interface UseApiOptions {
  onSuccess?: (data: any) => void;
  onError?: (error: string) => void;
  resetOnCall?: boolean;
}

export function useApi<T = any>(options: UseApiOptions = {}) {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (apiCall: () => Promise<T>) => {
      if (options.resetOnCall !== false) {
        setState({ data: null, loading: true, error: null });
      } else {
        setState(prev => ({ ...prev, loading: true, error: null }));
      }

      try {
        const result = await apiCall();
        setState({ data: result, loading: false, error: null });
        
        if (options.onSuccess) {
          options.onSuccess(result);
        }
        
        return result;
      } catch (error: any) {
        const errorMessage = error.message || 'An unexpected error occurred';
        setState({ data: null, loading: false, error: errorMessage });
        
        if (options.onError) {
          options.onError(errorMessage);
        }
        
        throw error;
      }
    },
    [options]
  );

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return {
    ...state,
    execute,
    reset,
  };
}

// Specialized hook for paginated API calls
export interface PaginatedApiState<T> extends ApiState<T[]> {
  page: number;
  totalPages: number;
  total: number;
  hasMore: boolean;
}

export function usePaginatedApi<T = any>(options: UseApiOptions = {}) {
  const [state, setState] = useState<PaginatedApiState<T>>({
    data: [],
    loading: false,
    error: null,
    page: 1,
    totalPages: 1,
    total: 0,
    hasMore: false,
  });

  const execute = useCallback(
    async (
      apiCall: (page: number, size: number) => Promise<{
        data?: T[];
        items?: T[];
        total: number;
        page: number;
        pages: number;
      }>,
      page: number = 1,
      size: number = 20,
      append: boolean = false
    ) => {
      setState(prev => ({ ...prev, loading: true, error: null }));

      try {
        const result = await apiCall(page, size);
        const items = result.data || result.items || [];
        
        setState(prev => ({
          data: append ? [...(prev.data || []), ...items] : items,
          loading: false,
          error: null,
          page: result.page,
          totalPages: result.pages,
          total: result.total,
          hasMore: result.page < result.pages,
        }));
        
        if (options.onSuccess) {
          options.onSuccess(result);
        }
        
        return result;
      } catch (error: any) {
        const errorMessage = error.message || 'An unexpected error occurred';
        setState(prev => ({ 
          ...prev, 
          loading: false, 
          error: errorMessage 
        }));
        
        if (options.onError) {
          options.onError(errorMessage);
        }
        
        throw error;
      }
    },
    [options]
  );

  const loadMore = useCallback(
    async (
      apiCall: (page: number, size: number) => Promise<any>,
      size: number = 20
    ) => {
      if (state.hasMore && !state.loading) {
        return execute(apiCall, state.page + 1, size, true);
      }
    },
    [state.hasMore, state.loading, state.page, execute]
  );

  const reset = useCallback(() => {
    setState({
      data: [],
      loading: false,
      error: null,
      page: 1,
      totalPages: 1,
      total: 0,
      hasMore: false,
    });
  }, []);

  return {
    ...state,
    execute,
    loadMore,
    reset,
  };
}

// Hook for form submissions with validation
export interface UseFormApiOptions<T> extends UseApiOptions {
  validate?: (data: T) => string | null;
}

export function useFormApi<T = any>(options: UseFormApiOptions<T> = {}) {
  const [state, setState] = useState<ApiState<any> & { validationError: string | null }>({
    data: null,
    loading: false,
    error: null,
    validationError: null,
  });

  const submit = useCallback(
    async (formData: T, apiCall: (data: T) => Promise<any>) => {
      // Reset validation error
      setState(prev => ({ ...prev, validationError: null }));

      // Validate if validator is provided
      if (options.validate) {
        const validationError = options.validate(formData);
        if (validationError) {
          setState(prev => ({ ...prev, validationError }));
          return;
        }
      }

      setState(prev => ({ ...prev, loading: true, error: null }));

      try {
        const result = await apiCall(formData);
        setState({ 
          data: result, 
          loading: false, 
          error: null, 
          validationError: null 
        });
        
        if (options.onSuccess) {
          options.onSuccess(result);
        }
        
        return result;
      } catch (error: any) {
        const errorMessage = error.message || 'An unexpected error occurred';
        setState({ 
          data: null, 
          loading: false, 
          error: errorMessage, 
          validationError: null 
        });
        
        if (options.onError) {
          options.onError(errorMessage);
        }
        
        throw error;
      }
    },
    [options]
  );

  const reset = useCallback(() => {
    setState({ 
      data: null, 
      loading: false, 
      error: null, 
      validationError: null 
    });
  }, []);

  return {
    ...state,
    submit,
    reset,
  };
}