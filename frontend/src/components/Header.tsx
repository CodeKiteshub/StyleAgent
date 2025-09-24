import React, { useState } from 'react';
import { Sparkles, Camera, MessageCircle, User, LogOut, Settings } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useToast } from './Toast';
import { LoadingButton } from './LoadingSpinner';
import { LoginModal } from './LoginModal';

export function Header() {
  const { user, isAuthenticated, logout, isLoading } = useAuth();
  const { success, error } = useToast();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginMode, setLoginMode] = useState<'login' | 'register'>('login');

  const handleLogout = async () => {
    try {
      await logout();
      success('Logged out successfully');
      setShowUserMenu(false);
    } catch (err) {
      error('Failed to logout', 'Please try again');
    }
  };

  const handleOpenLogin = (mode: 'login' | 'register') => {
    setLoginMode(mode);
    setShowLoginModal(true);
  };

  const handleSwitchMode = () => {
    setLoginMode(prev => prev === 'login' ? 'register' : 'login');
  };

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
          
          <div className="flex items-center space-x-4">
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

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 p-2 rounded-full hover:bg-gray-100 transition-colors"
                >
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">
                    {user?.username || 'User'}
                  </span>
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200">
                    <div className="px-4 py-2 text-sm text-gray-500 border-b border-gray-100">
                      {user?.email}
                    </div>
                    <button
                      onClick={() => setShowUserMenu(false)}
                      className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <Settings className="w-4 h-4 mr-2" />
                      Settings
                    </button>
                    <LoadingButton
                      loading={isLoading}
                      onClick={handleLogout}
                      className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      <LogOut className="w-4 h-4 mr-2" />
                      Logout
                    </LoadingButton>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button 
                  onClick={() => handleOpenLogin('login')}
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Login
                </button>
                <button 
                  onClick={() => handleOpenLogin('register')}
                  className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-medium rounded-md hover:from-purple-600 hover:to-pink-600 transition-colors"
                >
                  Sign Up
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        mode={loginMode}
        onSwitchMode={handleSwitchMode}
      />
    </header>
  );
}