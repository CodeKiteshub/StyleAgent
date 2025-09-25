import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { UserContext } from '../App';
import { chat as chatApi } from '../lib/api';

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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi there! I'm your personal fashion AI stylist ✨ I'll help you find the perfect outfits by understanding your style preferences. What's the occasion you're dressing for?",
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [userContext, setUserContext] = useState<UserContext>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const questions = [
    "What's the occasion you're dressing for? (e.g., casual brunch, work meeting, date night)",
    "What's your preferred style? (e.g., minimalist, streetwear, bohemian, classic)",
    "Any color preferences? (e.g., neutrals, bold colors, pastels)",
    "What's your budget range? (e.g., under $200, $200-500, $500+)"
  ];

  const contextKeys: (keyof UserContext)[] = ['occasion', 'style_preference', 'color_preference', 'budget'];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: currentMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newUserMessage]);

    // Call backend LLM chat
    setCurrentMessage('');
    try {
      const history = messages.map(m => ({ 
        role: (m.sender === 'ai' ? 'assistant' : 'user') as 'user' | 'assistant' | 'system', 
        content: m.text 
      }));
      const resp = await chatApi([...history, { role: 'user', content: currentMessage }]);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: resp.reply,
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);

      // Merge any extracted context
      const mergedContext: UserContext = {
        ...userContext,
        ...resp.user_context
      };
      setUserContext(mergedContext);

      // If we have all four keys, proceed to upload step automatically
      const haveAll = contextKeys.every(k => (mergedContext as any)[k]);
      if (haveAll) {
        onComplete(mergedContext);
      }
    } catch (e) {
      console.error('Chat API error:', e);
      console.error('Error type:', typeof e);
      console.error('Error message:', e instanceof Error ? e.message : String(e));
      console.error('Error stack:', e instanceof Error ? e.stack : 'No stack trace');
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
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
              disabled={!currentMessage.trim()}
              className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}