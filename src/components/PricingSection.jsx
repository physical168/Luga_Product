import React, { useState } from 'react';
import { Check } from 'lucide-react';

const PricingSection = () => {
  const [isAnnual, setIsAnnual] = useState(false);

  const teamFeatures = [
    '+20 Cutting-edge AI Models',
    '1200 AI Credits / month',
    'GPTs (AI Assistants)',
    'Prompts Library',
    'Advanced search',
    'Chat Folders'
  ];

  const enterpriseFeatures = [
    'Everything in Free',
    'Cutting-edge image generation',
    '1500 AI Credits / month',
    'DALL·E 3',
    'Stable Diffusion XL 1.0',
    'Stable Diffusion 1.6'
  ];

  return (
    <div className="py-32 bg-gradient-to-b from-purple-50 via-purple-50/50 to-transparent">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-medium mb-4">
            A simple pricing system.
          </h2>
          <h3 className="text-4xl font-medium mb-8">
            Select what works for you
          </h3>
          <p className="text-gray-600">
            Free 30-day trial, no credit card required.
          </p>
        </div>

        {/* Pricing Toggle */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex items-center bg-gray-100 rounded-full p-1">
            <button
              onClick={() => setIsAnnual(false)}
              className={`px-4 py-2 rounded-full text-sm ${
                !isAnnual ? 'bg-white shadow-sm' : ''
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setIsAnnual(true)}
              className={`px-4 py-2 rounded-full text-sm flex items-center space-x-2 ${
                isAnnual ? 'bg-white shadow-sm' : ''
              }`}
            >
              <span>Annual</span>
              <span className="text-xs text-purple-600 bg-purple-100 px-2 py-0.5 rounded-full">
                SAVE 30%
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 gap-8 max-w-4xl mx-auto">
          {/* Team Plan */}
          <div className="bg-white rounded-3xl p-8 shadow-lg">
            <h3 className="text-2xl font-medium mb-2 text-left">Team</h3>
            <p className="text-gray-600 mb-6 text-left">
              Boost your productivity with the power of generative AI.
            </p>
            <div className="mb-8 text-left">
              <span className="text-5xl font-medium">
                ${isAnnual ? '12' : '24'}/m
              </span>
            </div>
            <div className="space-y-4 mb-8">
              {teamFeatures.map((feature, index) => (
                <div key={index} className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>
            <button className="w-full py-3 text-center border border-gray-200 rounded-lg hover:border-gray-300 transition-colors">
              Get started
            </button>
          </div>

          {/* Enterprise Plan */}
          <div className="bg-white rounded-3xl p-8 shadow-lg relative overflow-hidden">
            <div className="absolute top-6 right-6">
              <span className="bg-purple-100 text-purple-600 text-xs px-3 py-1 rounded-full">
                Most popular
              </span>
            </div>
            <h3 className="text-2xl font-medium mb-2 text-left">Enterprise</h3>
            <p className="text-gray-600 mb-6 text-left">
              GPT-4 Turbo with unlimited access and advanced AI features.
            </p>
            <div className="mb-8 text-left">
              <span className="text-5xl font-medium">
                ${isAnnual ? '12' : '24'}/m
              </span>
            </div>
            <div className="space-y-4 mb-8">
              {enterpriseFeatures.map((feature, index) => (
                <div key={index} className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>
            <button className="w-full py-3 text-center bg-black text-white rounded-lg hover:bg-gray-800 transition-colors">
              Get started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingSection;