import React from 'react';
import { Menu, Settings, Moon, Sun, Trash2, User } from 'lucide-react';
import { cn } from '../utils/cn';

interface HeaderProps {
  user: { username: string; id: number };
  darkMode: boolean;
  onToggleSidebar: () => void;
  onToggleDarkMode: () => void;
  onClearChat: () => void;
  sidebarOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  user,
  darkMode,
  onToggleSidebar,
  onToggleDarkMode,
  onClearChat,
  sidebarOpen,
}) => {
  return (
    <header className="glass border-b border-white/20 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors lg:hidden"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 medical-gradient rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">AI</span>
            </div>
            <div>
              <h1 className="font-semibold text-slate-900">Medical Assistant</h1>
              <p className="text-xs text-slate-500">AI-Powered Health Guidance</p>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* User Info */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-white/50 rounded-full">
            <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="w-3 h-3 text-white" />
            </div>
            <span className="text-sm font-medium text-slate-700">
              {user.username}
            </span>
          </div>

          {/* Action Buttons */}
          <button
            onClick={onClearChat}
            className="p-2 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors"
            title="Clear Chat"
          >
            <Trash2 className="w-4 h-4" />
          </button>

          <button
            onClick={onToggleDarkMode}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            title="Toggle Dark Mode"
          >
            {darkMode ? (
              <Sun className="w-4 h-4" />
            ) : (
              <Moon className="w-4 h-4" />
            )}
          </button>

          <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};