import React from 'react';
import { Message } from '../types';
import { User, Bot, Clock } from 'lucide-react';
import { cn } from '../utils/cn';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={cn(
        'flex gap-3 p-4 chat-message',
        message.isUser ? 'flex-row-reverse' : 'flex-row'
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          message.isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
        )}
      >
        {message.isUser ? (
          <User className="w-4 h-4" />
        ) : (
          <Bot className="w-4 h-4" />
        )}
      </div>

      {/* Message Content */}
      <div
        className={cn(
          'flex flex-col max-w-[80%]',
          message.isUser ? 'items-end' : 'items-start'
        )}
      >
        <div
          className={cn(
            'rounded-2xl px-4 py-3 shadow-sm',
            message.isUser
              ? 'bg-blue-600 text-white rounded-br-md'
              : 'glass border rounded-bl-md'
          )}
        >
          {message.isUser ? (
            <p className="text-sm leading-relaxed">{message.content}</p>
          ) : (
            <div
              className="text-sm leading-relaxed prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: message.content }}
            />
          )}
        </div>

        {/* Timestamp */}
        <div
          className={cn(
            'flex items-center gap-1 mt-1 text-xs text-slate-500',
            message.isUser ? 'flex-row-reverse' : 'flex-row'
          )}
        >
          <Clock className="w-3 h-3" />
          <span>{formatTime(message.timestamp)}</span>
        </div>
      </div>
    </div>
  );
};