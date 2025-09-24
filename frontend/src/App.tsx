import React, { useState } from 'react';
import { Header } from './components/Header';
import { ChatInterface } from './components/ChatInterface';
import { ImageUpload } from './components/ImageUpload';
import { OutfitRecommendations } from './components/OutfitRecommendations';
import { LoadingAnalysis } from './components/LoadingAnalysis';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';
import { AuthProvider } from './hooks/useAuth';
import { TestApiPanel } from './components/TestApiPanel';

export interface UserContext {
  occasion?: string;
  style_preference?: string;
  body_type?: string;
  color_preference?: string;
  budget?: string;
}

export interface OutfitRecommendation {
  id: string;
  image_url: string;
  title: string;
  caption: string;
  hashtags: string[];
  price_range: {
    min: number;
    max: number;
    currency: string;
  };
  body_fit: string;
  trend_score: number;
  social_stats: {
    likes: number;
    shares: number;
    saves: number;
  };
}

function App() {
  const [currentStep, setCurrentStep] = useState<'chat' | 'upload' | 'analysis' | 'results'>('chat');
  const [userContext, setUserContext] = useState<UserContext>({});
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<OutfitRecommendation[]>([]);

  const handleChatComplete = (context: UserContext) => {
    setUserContext(context);
    setCurrentStep('upload');
  };

  const handleImageUpload = (imageUrl: string) => {
    setUploadedImage(imageUrl);
    setCurrentStep('analysis');
    
    // Simulate AI analysis delay
    setTimeout(() => {
      generateRecommendations();
    }, 3000);
  };

  const generateRecommendations = () => {
    // Mock AI-generated recommendations based on user context
    const mockRecommendations: OutfitRecommendation[] = [
      {
        id: '1',
        image_url: 'https://images.pexels.com/photos/1661471/pexels-photo-1661471.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Chic Minimalist Look',
        caption: 'Perfect for your casual brunch! Clean lines and neutral tones that complement your style perfectly ✨',
        hashtags: ['#minimalist', '#brunch', '#casualchic', '#neutrals', '#effortless'],
        price_range: { min: 150, max: 250, currency: 'USD' },
        body_fit: '95% match',
        trend_score: 92,
        social_stats: { likes: 2847, shares: 156, saves: 89 }
      },
      {
        id: '2',
        image_url: 'https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Urban Streetwear Vibe',
        caption: 'Street style meets comfort - this outfit screams confidence and modern edge 🔥',
        hashtags: ['#streetwear', '#urban', '#confident', '#edgy', '#trendy'],
        price_range: { min: 200, max: 350, currency: 'USD' },
        body_fit: '88% match',
        trend_score: 96,
        social_stats: { likes: 4231, shares: 298, saves: 156 }
      },
      {
        id: '3',
        image_url: 'https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Classic Professional',
        caption: 'Timeless elegance for any professional setting. Sharp, sophisticated, and always appropriate 💼',
        hashtags: ['#professional', '#classic', '#elegant', '#workwear', '#sophisticated'],
        price_range: { min: 300, max: 450, currency: 'USD' },
        body_fit: '90% match',
        trend_score: 78,
        social_stats: { likes: 1689, shares: 89, saves: 67 }
      },
      {
        id: '4',
        image_url: 'https://images.pexels.com/photos/1324463/pexels-photo-1324463.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Casual Weekend Comfort',
        caption: 'Weekend vibes done right! Comfort meets style in this relaxed yet put-together look 🌟',
        hashtags: ['#weekend', '#casual', '#comfortable', '#relaxed', '#effortless'],
        price_range: { min: 100, max: 180, currency: 'USD' },
        body_fit: '93% match',
        trend_score: 85,
        social_stats: { likes: 3456, shares: 203, saves: 134 }
      },
      {
        id: '5',
        image_url: 'https://images.pexels.com/photos/1139743/pexels-photo-1139743.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Date Night Ready',
        caption: 'Dinner date perfection! This look balances sophistication with a hint of playfulness 💕',
        hashtags: ['#datenight', '#romantic', '#sophisticated', '#elegant', '#dinner'],
        price_range: { min: 180, max: 280, currency: 'USD' },
        body_fit: '91% match',
        trend_score: 89,
        social_stats: { likes: 2934, shares: 167, saves: 98 }
      },
      {
        id: '6',
        image_url: 'https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=400',
        title: 'Bohemian Chic',
        caption: 'Free-spirited and fabulous! This boho look is perfect for music festivals or artistic events 🌸',
        hashtags: ['#boho', '#bohemian', '#artistic', '#freespirit', '#festival'],
        price_range: { min: 120, max: 200, currency: 'USD' },
        body_fit: '87% match',
        trend_score: 82,
        social_stats: { likes: 1823, shares: 134, saves: 76 }
      }
    ];

    setRecommendations(mockRecommendations);
    setCurrentStep('results');
  };

  const resetApp = () => {
    setCurrentStep('chat');
    setUserContext({});
    setUploadedImage(null);
    setRecommendations([]);
  };

  return (
    <ErrorBoundary>
      <AuthProvider>
        <ToastProvider>
          <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
            <Header />
            
            <main className="container mx-auto px-4 py-6 max-w-4xl">
              {/* Add TestApiPanel for testing */}
              <TestApiPanel />
              
              {currentStep === 'chat' && (
                <ChatInterface onComplete={handleChatComplete} />
              )}
              
              {currentStep === 'upload' && (
                <ImageUpload onUpload={handleImageUpload} userContext={userContext} />
              )}
              
              {currentStep === 'analysis' && (
                <LoadingAnalysis userContext={userContext} />
              )}
              
              {currentStep === 'results' && (
                <OutfitRecommendations
                  recommendations={recommendations}
                  userContext={userContext}
                  onReset={resetApp}
                />
              )}
            </main>
          </div>
        </ToastProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;