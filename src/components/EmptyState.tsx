import React from 'react';
import { MessageSquare, Shield, Clock, Users } from 'lucide-react';

export const EmptyState: React.FC = () => {
  const features = [
    {
      icon: MessageSquare,
      title: 'Ask Medical Questions',
      description: 'Get instant responses to your health concerns and symptoms',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your conversations are confidential and protected',
    },
    {
      icon: Clock,
      title: '24/7 Availability',
      description: 'Access medical guidance anytime, anywhere',
    },
    {
      icon: Users,
      title: 'Professional Guidance',
      description: 'AI-powered responses based on medical knowledge',
    },
  ];

  const suggestions = [
    "I have a headache and feel dizzy",
    "What are the symptoms of the flu?",
    "I'm experiencing chest pain",
    "How can I manage my diabetes?",
    "What should I do for a sprained ankle?",
  ];

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl mx-auto text-center">
        {/* Hero Section */}
        <div className="mb-12">
          <div className="w-16 h-16 medical-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
            <MessageSquare className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-slate-900 mb-4">
            Welcome to Your Medical Assistant
          </h2>
          <p className="text-lg text-slate-600 leading-relaxed">
            I'm here to help you with medical questions and health concerns. 
            Start by describing your symptoms or asking a health-related question.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass rounded-xl p-6 text-left hover:shadow-lg transition-shadow"
            >
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <feature.icon className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-slate-900 mb-2">{feature.title}</h3>
              <p className="text-sm text-slate-600">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Quick Suggestions */}
        <div className="text-left">
          <h3 className="font-semibold text-slate-900 mb-4">Try asking about:</h3>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="px-4 py-2 bg-white/60 hover:bg-white/80 border border-slate-200 rounded-full text-sm text-slate-700 transition-colors hover:border-blue-300"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-12 p-4 bg-amber-50 border border-amber-200 rounded-xl">
          <p className="text-sm text-amber-800">
            <strong>Important:</strong> This AI provides general health information only. 
            Always consult with qualified healthcare professionals for medical advice, 
            diagnosis, or treatment. In case of emergency, contact your local emergency services.
          </p>
        </div>
      </div>
    </div>
  );
};