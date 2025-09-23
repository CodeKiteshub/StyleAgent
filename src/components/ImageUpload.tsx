import React, { useState, useRef } from 'react';
import { Upload, Camera, Image as ImageIcon, Sparkles } from 'lucide-react';
import { UserContext } from '../App';

interface Props {
  onUpload: (imageUrl: string) => void;
  userContext: UserContext;
}

export function ImageUpload({ onUpload, userContext }: Props) {
  const [dragOver, setDragOver] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFile = (file: File) => {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setImagePreview(result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = () => {
    if (imagePreview) {
      onUpload(imagePreview);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Your Photo</h2>
        <p className="text-gray-600">I'll analyze your body type, current style, and recommend perfect outfits!</p>
      </div>

      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
        <div className="mb-6">
          <h3 className="font-semibold text-gray-900 mb-3">Your Style Profile:</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-purple-50 p-3 rounded-lg">
              <p className="text-sm font-medium text-purple-900">Occasion</p>
              <p className="text-purple-700">{userContext.occasion || 'Not specified'}</p>
            </div>
            <div className="bg-pink-50 p-3 rounded-lg">
              <p className="text-sm font-medium text-pink-900">Style</p>
              <p className="text-pink-700">{userContext.style_preference || 'Not specified'}</p>
            </div>
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-sm font-medium text-blue-900">Colors</p>
              <p className="text-blue-700">{userContext.color_preference || 'Not specified'}</p>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <p className="text-sm font-medium text-green-900">Budget</p>
              <p className="text-green-700">{userContext.budget || 'Not specified'}</p>
            </div>
          </div>
        </div>

        {!imagePreview ? (
          <div
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
              dragOver 
                ? 'border-purple-500 bg-purple-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="space-y-4">
              <div className="flex justify-center">
                <div className="p-3 bg-gray-100 rounded-full">
                  <ImageIcon className="w-8 h-8 text-gray-400" />
                </div>
              </div>
              <div>
                <p className="text-lg font-medium text-gray-900">Drop your photo here</p>
                <p className="text-gray-500">or click to browse</p>
              </div>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Choose File
                </button>
                <button className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  <Camera className="w-4 h-4 mr-2" />
                  Take Photo
                </button>
              </div>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileInput}
              className="hidden"
            />
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative">
              <img 
                src={imagePreview} 
                alt="Preview" 
                className="w-full h-64 object-cover rounded-lg shadow-md"
              />
              <button
                onClick={() => setImagePreview(null)}
                className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
              >
                ×
              </button>
            </div>
            
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg">
              <div className="flex items-center mb-2">
                <Sparkles className="w-5 h-5 text-purple-600 mr-2" />
                <h4 className="font-semibold text-gray-900">AI Analysis Ready</h4>
              </div>
              <p className="text-sm text-gray-600 mb-4">
                I'll analyze your body type, detect current clothing style, and check social media trends to find the perfect outfits for you!
              </p>
              <button
                onClick={handleAnalyze}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-6 rounded-lg font-medium hover:shadow-lg transition-all"
              >
                Analyze & Get Recommendations ✨
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}