import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  isLoading = false,
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <div className="border-t border-slate-200 bg-white/80 backdrop-blur-sm p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative flex items-end gap-3">
          {/* Text Input */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe your symptoms or ask a medical question..."
              disabled={disabled || isLoading}
              className={cn(
                'w-full resize-none rounded-2xl border border-slate-300 px-4 py-3 pr-12',
                'focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20',
                'disabled:opacity-50 disabled:cursor-not-allowed',
                'placeholder:text-slate-400 text-sm leading-relaxed',
                'min-h-[48px] max-h-32 scrollbar-thin'
              )}
              rows={1}
            />
            
            {/* Voice Input Button */}
            <button
              type="button"
              className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-slate-400 hover:text-slate-600 transition-colors"
              disabled={disabled || isLoading}
            >
              <Mic className="w-4 h-4" />
            </button>
          </div>

          {/* Send Button */}
          <button
            type="submit"
            disabled={!message.trim() || disabled || isLoading}
            className={cn(
              'flex-shrink-0 w-12 h-12 rounded-2xl medical-gradient text-white',
              'flex items-center justify-center transition-all duration-200',
              'hover:shadow-lg hover:scale-105 active:scale-95',
              'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100'
            )}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Disclaimer */}
        <p className="text-xs text-slate-500 mt-3 text-center">
          This AI provides general health information only. Always consult healthcare professionals for medical advice.
        </p>
      </form>
    </div>
  );
};