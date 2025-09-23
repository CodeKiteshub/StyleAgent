import React from 'react';
import { Sparkles, Camera, MessageCircle } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                StyleAI
              </h1>
              <p className="text-xs text-gray-500">Powered by RAG + Computer Vision</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-1">
            <div className="flex items-center px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-600">
              <MessageCircle className="w-4 h-4 mr-1" />
              Chat
            </div>
            <div className="flex items-center px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-600">
              <Camera className="w-4 h-4 mr-1" />
              Analyze
            </div>
            <div className="flex items-center px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full text-sm">
              <Sparkles className="w-4 h-4 mr-1" />
              Recommend
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}