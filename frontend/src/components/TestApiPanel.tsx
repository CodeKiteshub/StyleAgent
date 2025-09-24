import React, { useState } from 'react';
import { Upload, Image, MessageSquare, Sparkles, User, Heart } from 'lucide-react';
import { useToast } from './Toast';
import { LoadingButton } from './LoadingSpinner';
import { imageService } from '../services/imageService';
import { chatService } from '../services/chatService';
import { userService } from '../services/userService';
import { recommendationService } from '../services/recommendationService';

export function TestApiPanel() {
  const [isLoading, setIsLoading] = useState(false);
  const [testResults, setTestResults] = useState<string[]>([]);
  const { success, error } = useToast();

  const addResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testImageUpload = async () => {
    setIsLoading(true);
    try {
      // Test with a sample image URL
      const result = await imageService.uploadImageFromUrl('https://via.placeholder.com/300x400/FF6B6B/FFFFFF?text=Test+Outfit');
      addResult(`✅ Image upload successful: ${result.id}`);
      success('Image API Test', 'Image upload successful');
    } catch (err: any) {
      addResult(`❌ Image upload failed: ${err.message}`);
      error('Image API Test', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const testChatMessage = async () => {
    setIsLoading(true);
    try {
      const conversation = await chatService.createConversation({
        title: 'Test Chat'
      });
      
      const message = await chatService.sendMessage(conversation.id, {
        content: 'What colors work well with navy blue?'
      });
      
      addResult(`✅ Chat test successful: Created conversation ${conversation.id} and sent message`);
      success('Chat API Test', 'Chat functionality working');
    } catch (err: any) {
      addResult(`❌ Chat test failed: ${err.message}`);
      error('Chat API Test', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const testRecommendations = async () => {
    setIsLoading(true);
    try {
      const recommendations = await recommendationService.getRecommendations({
        limit: 5,
        user_context: {
          style_preference: 'casual'
        }
      });
      
      addResult(`✅ Recommendations test successful: Got ${recommendations.length} items`);
      success('Recommendations API Test', `Retrieved ${recommendations.length} recommendations`);
    } catch (err: any) {
      addResult(`❌ Recommendations test failed: ${err.message}`);
      error('Recommendations API Test', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const testUserProfile = async () => {
    setIsLoading(true);
    try {
      const profile = await userService.getProfile();
      addResult(`✅ User profile test successful: ${profile.username}`);
      success('User API Test', 'Profile retrieved successfully');
    } catch (err: any) {
      addResult(`❌ User profile test failed: ${err.message}`);
      error('User API Test', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setTestResults([]);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">API Test Panel</h2>
        <button
          onClick={clearResults}
          className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded"
        >
          Clear Results
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <LoadingButton
          loading={isLoading}
          onClick={testImageUpload}
          className="flex items-center justify-center p-4 border-2 border-dashed border-purple-300 rounded-lg hover:border-purple-400 transition-colors"
        >
          <Upload className="w-5 h-5 mr-2" />
          Test Image Upload
        </LoadingButton>

        <LoadingButton
          loading={isLoading}
          onClick={testChatMessage}
          className="flex items-center justify-center p-4 border-2 border-dashed border-blue-300 rounded-lg hover:border-blue-400 transition-colors"
        >
          <MessageSquare className="w-5 h-5 mr-2" />
          Test Chat API
        </LoadingButton>

        <LoadingButton
          loading={isLoading}
          onClick={testRecommendations}
          className="flex items-center justify-center p-4 border-2 border-dashed border-green-300 rounded-lg hover:border-green-400 transition-colors"
        >
          <Sparkles className="w-5 h-5 mr-2" />
          Test Recommendations
        </LoadingButton>

        <LoadingButton
          loading={isLoading}
          onClick={testUserProfile}
          className="flex items-center justify-center p-4 border-2 border-dashed border-orange-300 rounded-lg hover:border-orange-400 transition-colors"
        >
          <User className="w-5 h-5 mr-2" />
          Test User Profile
        </LoadingButton>
      </div>

      {testResults.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Test Results</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {testResults.map((result, index) => (
              <div
                key={index}
                className={`p-2 rounded text-sm font-mono ${
                  result.includes('✅')
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {result}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">Testing Instructions</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Make sure you're logged in before testing user-specific APIs</li>
          <li>• Image upload test uses a placeholder image URL</li>
          <li>• Chat test creates a new conversation and sends a message</li>
          <li>• Recommendations test fetches personalized suggestions</li>
          <li>• User profile test requires authentication</li>
        </ul>
      </div>
    </div>
  );
}