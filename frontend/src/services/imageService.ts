import apiClient, { handleApiResponse, handleApiError } from './api';

// Image types
export interface ImageAnalysisResult {
  id: string;
  image_url: string;
  analysis: {
    clothing_items: ClothingItem[];
    colors: ColorAnalysis[];
    style_tags: string[];
    occasion_suitability: string[];
    body_type_compatibility: string[];
    confidence_score: number;
  };
  created_at: string;
}

export interface ClothingItem {
  type: string;
  color: string;
  pattern?: string;
  material?: string;
  brand?: string;
  confidence: number;
  bounding_box?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

export interface ColorAnalysis {
  color: string;
  hex_code: string;
  percentage: number;
  dominant: boolean;
}

export interface ImageUploadResponse {
  id: string;
  url: string;
  filename: string;
  size: number;
  content_type: string;
  created_at: string;
}

export interface OutfitAnalysisRequest {
  image_url: string;
  context?: {
    occasion?: string;
    style_preference?: string;
    body_type?: string;
    budget?: string;
  };
}

export interface StyleTransferRequest {
  source_image_url: string;
  style_reference_url: string;
  intensity?: number; // 0.1 to 1.0
}

export interface StyleTransferResult {
  id: string;
  result_image_url: string;
  source_image_url: string;
  style_reference_url: string;
  processing_time: number;
  created_at: string;
}

class ImageService {
  // Upload image file
  async uploadImage(file: File): Promise<ImageUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post('/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return handleApiResponse<ImageUploadResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Upload image from URL
  async uploadImageFromUrl(imageUrl: string): Promise<ImageUploadResponse> {
    try {
      const response = await apiClient.post('/images/upload-url', {
        image_url: imageUrl,
      });

      return handleApiResponse<ImageUploadResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Analyze outfit in image
  async analyzeOutfit(request: OutfitAnalysisRequest): Promise<ImageAnalysisResult> {
    try {
      const response = await apiClient.post('/images/analyze', request);
      return handleApiResponse<ImageAnalysisResult>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get analysis result by ID
  async getAnalysisResult(analysisId: string): Promise<ImageAnalysisResult> {
    try {
      const response = await apiClient.get(`/images/analysis/${analysisId}`);
      return handleApiResponse<ImageAnalysisResult>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get user's image analysis history
  async getAnalysisHistory(
    page: number = 1,
    size: number = 20
  ): Promise<{
    analyses: ImageAnalysisResult[];
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

      const response = await apiClient.get(`/images/history?${params.toString()}`);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Perform style transfer
  async performStyleTransfer(request: StyleTransferRequest): Promise<StyleTransferResult> {
    try {
      const response = await apiClient.post('/images/style-transfer', request);
      return handleApiResponse<StyleTransferResult>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get style transfer result
  async getStyleTransferResult(transferId: string): Promise<StyleTransferResult> {
    try {
      const response = await apiClient.get(`/images/style-transfer/${transferId}`);
      return handleApiResponse<StyleTransferResult>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Delete uploaded image
  async deleteImage(imageId: string): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete(`/images/${imageId}`);
      return handleApiResponse<{ message: string }>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get image metadata
  async getImageMetadata(imageId: string): Promise<ImageUploadResponse> {
    try {
      const response = await apiClient.get(`/images/${imageId}/metadata`);
      return handleApiResponse<ImageUploadResponse>(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Batch analyze multiple images
  async batchAnalyze(
    imageUrls: string[],
    context?: any
  ): Promise<{ analyses: ImageAnalysisResult[]; batch_id: string }> {
    try {
      const response = await apiClient.post('/images/batch-analyze', {
        image_urls: imageUrls,
        context,
      });
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }

  // Get batch analysis status
  async getBatchAnalysisStatus(
    batchId: string
  ): Promise<{
    batch_id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    results?: ImageAnalysisResult[];
  }> {
    try {
      const response = await apiClient.get(`/images/batch/${batchId}`);
      return handleApiResponse(response);
    } catch (error: any) {
      throw new Error(handleApiError(error));
    }
  }
}

// Export singleton instance
export const imageService = new ImageService();
export default imageService;