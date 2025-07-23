import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './components/ChatMessage';
import { TypingIndicator } from './components/TypingIndicator';
import { ChatInput } from './components/ChatInput';
import { EmptyState } from './components/EmptyState';
import { Message } from './types';
import { chatApi } from './services/api';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [user] = useState({ username: 'Guest', id: 0 });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // For now, we'll simulate the API call since your backend redirects
      // You may need to modify your backend to return JSON responses
      const response = await simulateApiCall(content);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Temporary simulation - replace with actual API call
  const simulateApiCall = async (message: string): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    return `
      <p><strong>Thank you for your question about:</strong> ${message}</p>
      
      <h3>Possible Causes:</h3>
      <ul>
        <li><strong>Stress or tension</strong> - Common cause of various symptoms</li>
        <li><strong>Dehydration</strong> - Can lead to headaches and fatigue</li>
        <li><strong>Lack of sleep</strong> - Affects overall health and wellbeing</li>
        <li><strong>Environmental factors</strong> - Weather, allergens, or air quality</li>
      </ul>
      
      <h3>General Recommendations:</h3>
      <ul>
        <li><strong>Rest:</strong> Get adequate sleep and take breaks when needed</li>
        <li><strong>Hydration:</strong> Drink plenty of water throughout the day</li>
        <li><strong>Healthy lifestyle:</strong> Maintain a balanced diet and regular exercise</li>
        <li><strong>Monitor symptoms:</strong> Keep track of when symptoms occur</li>
      </ul>
      
      <p><strong>Disclaimer:</strong> This information is for general guidance only. Always consult a healthcare professional for personalized advice, diagnosis, or treatment.</p>
    `;
  };

  const handleClearChat = async () => {
    try {
      await chatApi.clearChat();
      setMessages([]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const handleToggleDarkMode = async () => {
    try {
      await chatApi.toggleDarkMode();
      setDarkMode(!darkMode);
    } catch (error) {
      console.error('Error toggling dark mode:', error);
    }
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <Header
          user={user}
          darkMode={darkMode}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onToggleDarkMode={handleToggleDarkMode}
          onClearChat={handleClearChat}
          sidebarOpen={sidebarOpen}
        />

        {/* Chat Area */}
        <div className="flex-1 flex flex-col min-h-0">
          <div className="flex-1 overflow-y-auto scrollbar-thin">
            {messages.length === 0 ? (
              <EmptyState />
            ) : (
              <div className="max-w-4xl mx-auto">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                {isLoading && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Chat Input */}
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={isLoading}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}

export default App;