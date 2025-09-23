import React, { useState, useEffect } from 'react';
import { Brain, Camera, TrendingUp, Sparkles } from 'lucide-react';
import { UserContext } from '../App';

interface Props {
  userContext: UserContext;
}

export function LoadingAnalysis({ userContext }: Props) {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  const analysisSteps = [
    {
      icon: Camera,
      title: 'Computer Vision Analysis',
      description: 'Analyzing body proportions and current outfit style using OpenPose + CLIP-ViT',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Brain,
      title: 'RAG Retrieval Process',
      description: 'Searching 10,000+ outfit database using Pinecone vector similarity',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: TrendingUp,
      title: 'Social Media Trend Analysis',
      description: 'Analyzing Instagram & TikTok trends for viral potential scoring',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: Sparkles,
      title: 'AI Recommendation Generation',
      description: 'GPT-4 generating personalized outfit recommendations with styling tips',
      color: 'from-green-500 to-teal-500'
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 2;
      });
    }, 60);

    const stepInterval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev >= analysisSteps.length - 1) {
          clearInterval(stepInterval);
          return prev;
        }
        return prev + 1;
      });
    }, 750);

    return () => {
      clearInterval(interval);
      clearInterval(stepInterval);
    };
  }, []);

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mb-4">
          <Sparkles className="w-8 h-8 text-white animate-pulse" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing Your Style</h2>
        <p className="text-gray-600">Our AI is working its magic to find perfect outfits for you!</p>
      </div>

      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Processing</span>
            <span className="text-sm font-medium text-gray-700">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="space-y-4">
          {analysisSteps.map((step, index) => {
            const Icon = step.icon;
            const isActive = index <= currentStep;
            const isCompleted = index < currentStep;
            
            return (
              <div 
                key={index}
                className={`flex items-start p-4 rounded-lg transition-all duration-500 ${
                  isActive 
                    ? 'bg-gradient-to-r from-gray-50 to-purple-50 border border-purple-200' 
                    : 'bg-gray-50'
                }`}
              >
                <div className={`p-2 rounded-lg mr-4 ${
                  isActive 
                    ? `bg-gradient-to-r ${step.color} text-white ${!isCompleted ? 'animate-pulse' : ''}` 
                    : 'bg-gray-200 text-gray-400'
                }`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <h4 className={`font-semibold ${isActive ? 'text-gray-900' : 'text-gray-500'}`}>
                    {step.title}
                    {isCompleted && <span className="ml-2 text-green-500">✓</span>}
                    {isActive && !isCompleted && <span className="ml-2 text-blue-500 animate-pulse">...</span>}
                  </h4>
                  <p className={`text-sm ${isActive ? 'text-gray-600' : 'text-gray-400'}`}>
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
          <h4 className="font-semibold text-gray-900 mb-2">Your Style Context:</h4>
          <div className="text-sm text-gray-600 space-y-1">
            <p><span className="font-medium">Occasion:</span> {userContext.occasion}</p>
            <p><span className="font-medium">Style:</span> {userContext.style_preference}</p>
            <p><span className="font-medium">Colors:</span> {userContext.color_preference}</p>
            <p><span className="font-medium">Budget:</span> {userContext.budget}</p>
          </div>
        </div>
      </div>
    </div>
  );
}