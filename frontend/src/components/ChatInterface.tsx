import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Loader2 } from 'lucide-react';
import { UserContext } from '../App';
import { chatService, ChatMessage } from '../services/chatService';
import { useToast } from './Toast';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface Props {
  onComplete: (context: UserContext) => void;
}

export function ChatInterface({ onComplete }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [userContext, setUserContext] = useState<UserContext>({});
  const [messageCount, setMessageCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { error } = useToast();

  // Initialize conversation when component mounts
  useEffect(() => {
    initializeConversation();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeConversation = async () => {
    try {
      setIsLoading(true);
      const conversation = await chatService.createConversation({
        title: 'Style Consultation',
        initial_message: "Hi! I'm your personal fashion AI stylist ✨ I'll help you find the perfect outfits by understanding your style preferences. What's the occasion you're dressing for?"
      });
      
      setConversationId(conversation.id);
      
      // Add the initial AI message
      const initialMessage: Message = {
        id: '1',
        text: "Hi! I'm your personal fashion AI stylist ✨ I'll help you find the perfect outfits by understanding your style preferences. What's the occasion you're dressing for?",
        sender: 'ai',
        timestamp: new Date()
      };
      
      setMessages([initialMessage]);
    } catch (err: any) {
      error('Chat Error', 'Failed to initialize chat. Please try again.');
      console.error('Failed to initialize conversation:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const extractContextFromMessage = (message: string, messageNumber: number): Partial<UserContext> => {
    // Simple context extraction based on message order and content
    const context: Partial<UserContext> = {};
    
    if (messageNumber === 1) {
      context.occasion = message;
    } else if (messageNumber === 2) {
      context.style_preference = message;
    } else if (messageNumber === 3) {
      context.color_preference = message;
    } else if (messageNumber === 4) {
      context.budget = message;
    }
    
    return context;
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || !conversationId || isLoading) return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: currentMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newUserMessage]);
    
    // Extract context from user message
    const newContext = extractContextFromMessage(currentMessage, messageCount + 1);
    const updatedContext = { ...userContext, ...newContext };
    setUserContext(updatedContext);
    setMessageCount(prev => prev + 1);

    const messageText = currentMessage;
    setCurrentMessage('');
    setIsLoading(true);

    try {
      // Send message to backend with context
      const response = await chatService.sendMessage(conversationId, {
        content: messageText,
        context: updatedContext
      });

      // Add AI response to messages
      const aiMessage: Message = {
        id: response.message.id,
        text: response.message.content,
        sender: 'ai',
        timestamp: new Date(response.message.timestamp)
      };

      setMessages(prev => [...prev, aiMessage]);

      // Check if we have enough context to proceed to next step
      if (messageCount >= 3 && updatedContext.occasion && updatedContext.style_preference) {
        setTimeout(() => {
          onComplete(updatedContext);
        }, 1000);
      }

    } catch (err: any) {
      error('Chat Error', 'Failed to send message. Please try again.');
      console.error('Failed to send message:', err);
      
      // Add fallback AI response
      const fallbackMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble connecting right now. Could you please try again?",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4">
          <h2 className="text-white text-lg font-semibold">Fashion Consultation</h2>
          <p className="text-purple-100 text-sm">Let's understand your style preferences</p>
        </div>

        <div className="h-96 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                  message.sender === 'user'
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {message.sender === 'ai' && (
                  <div className="flex items-center mb-1">
                    <Sparkles className="w-4 h-4 mr-1 text-purple-600" />
                    <span className="text-xs font-medium text-purple-600">StyleAI</span>
                  </div>
                )}
                <p className="text-sm leading-relaxed">{message.text}</p>
                <p className={`text-xs mt-1 ${
                  message.sender === 'user' ? 'text-purple-100' : 'text-gray-500'
                }`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-gray-100">
          <div className="flex space-x-2">
            <input
              type="text"
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your response..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
            <button
              onClick={handleSendMessage}
              disabled={!currentMessage.trim() || isLoading}
              className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}