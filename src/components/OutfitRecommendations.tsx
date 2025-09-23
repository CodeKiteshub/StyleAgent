import React from 'react';
import { Share2, Heart, MessageCircle, Bookmark, RotateCcw, TrendingUp, DollarSign } from 'lucide-react';
import { OutfitRecommendation, UserContext } from '../App';

interface Props {
  recommendations: OutfitRecommendation[];
  userContext: UserContext;
  onReset: () => void;
}

export function OutfitRecommendations({ recommendations, userContext, onReset }: Props) {
  const handleShare = (outfit: OutfitRecommendation) => {
    if (navigator.share) {
      navigator.share({
        title: `StyleAI Recommendation: ${outfit.title}`,
        text: outfit.caption,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(
        `Check out this amazing outfit recommendation from StyleAI! ${outfit.title}: ${outfit.caption} ${outfit.hashtags.join(' ')}`
      );
      alert('Outfit details copied to clipboard!');
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Perfect Outfits ✨</h2>
        <p className="text-gray-600 mb-4">
          Curated just for you based on AI analysis of your style, body type, and current trends
        </p>
        <button
          onClick={onReset}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <RotateCcw className="w-4 h-4 mr-2" />
          Start New Analysis
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mb-6">
        <h3 className="font-semibold text-gray-900 mb-3">Analysis Summary:</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm font-medium text-purple-900">Occasion</p>
            <p className="text-purple-700 font-semibold">{userContext.occasion}</p>
          </div>
          <div className="bg-pink-50 p-4 rounded-lg">
            <p className="text-sm font-medium text-pink-900">Style Preference</p>
            <p className="text-pink-700 font-semibold">{userContext.style_preference}</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm font-medium text-blue-900">Color Palette</p>
            <p className="text-blue-700 font-semibold">{userContext.color_preference}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm font-medium text-green-900">Budget Range</p>
            <p className="text-green-700 font-semibold">{userContext.budget}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((outfit, index) => (
          <div key={outfit.id} className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:scale-[1.02]">
            <div className="relative">
              <img 
                src={outfit.image_url} 
                alt={outfit.title}
                className="w-full h-64 object-cover"
              />
              <div className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium">
                #{index + 1} Recommendation
              </div>
              <div className="absolute top-3 right-3 flex space-x-2">
                <div className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {outfit.trend_score}%
                </div>
              </div>
            </div>
            
            <div className="p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-lg text-gray-900">{outfit.title}</h3>
                <div className="flex items-center space-x-1 text-sm text-green-600 font-medium">
                  <DollarSign className="w-4 h-4" />
                  {outfit.price_range}
                </div>
              </div>
              
              <p className="text-gray-700 text-sm leading-relaxed mb-3">
                {outfit.caption}
              </p>
              
              <div className="flex flex-wrap gap-1 mb-4">
                {outfit.hashtags.map((tag, tagIndex) => (
                  <span 
                    key={tagIndex}
                    className="text-xs bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 px-2 py-1 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-3">
                  <span className="flex items-center">
                    <Heart className="w-4 h-4 mr-1 text-red-500" />
                    {outfit.social_stats.likes.toLocaleString()}
                  </span>
                  <span className="flex items-center">
                    <Share2 className="w-4 h-4 mr-1 text-blue-500" />
                    {outfit.social_stats.shares}
                  </span>
                </div>
                <div className="bg-blue-50 px-2 py-1 rounded-full text-blue-700 text-xs font-medium">
                  {outfit.body_fit} body match
                </div>
              </div>

              <div className="flex space-x-2">
                <button 
                  onClick={() => handleShare(outfit)}
                  className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white py-2 px-4 rounded-lg font-medium hover:shadow-lg transition-all text-sm"
                >
                  Share Outfit
                </button>
                <button className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <Bookmark className="w-4 h-4 text-gray-600" />
                </button>
                <button className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <MessageCircle className="w-4 h-4 text-gray-600" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Love Your Recommendations?</h3>
        <p className="text-gray-600 mb-4">Get personalized styling tips and outfit updates delivered weekly!</p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center max-w-md mx-auto">
          <input 
            type="email" 
            placeholder="Enter your email"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg transition-all">
            Subscribe
          </button>
        </div>
      </div>
    </div>
  );
}