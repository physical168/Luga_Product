import React, { useState } from 'react';
import { Play, Volume2, Maximize2, MoreVertical } from 'lucide-react';

const TextToVideo = () => {
  const [text, setText] = useState('');

  return (
    <div className="flex-1 flex space-x-4">
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-white rounded-2xl overflow-hidden shadow-sm">
        <div className="flex-1 p-8 flex flex-col">
          {/* Text Input Area */}
          <div className="flex-1">
            <textarea
              placeholder="Start typing here or paste any text you want to generate Lip Sync Video"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-[calc(100vh-240px)] p-6 border rounded-2xl resize-none focus:outline-none focus:border-gray-400 text-base text-gray-500"
            />
          </div>

          {/* Buttons */}
          <div className="flex items-center justify-between mt-6 space-x-4">
            <div className="flex space-x-4">
              <button className="rounded-full px-4 py-2 border border-gray-200 hover:bg-gray-50 flex items-center space-x-2">
                <span className="text-sm">Choose from audio history</span>
              </button>
              <button className="rounded-full px-4 py-2 border border-gray-200 hover:bg-gray-50 flex items-center space-x-2">
                <span className="text-sm">Upload an audio</span>
              </button>
            </div>
            <button className="rounded-full px-6 py-2 bg-black text-white hover:bg-gray-800 flex items-center space-x-2">
              <span className="text-sm">Lip Sync</span>
            </button>
          </div>
        </div>
      </div>

      {/* Video Preview Area - Right Side */}
      <div className="w-96 space-y-4">
        {/* First Video */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="relative aspect-[4/5] bg-gray-100 rounded-xl overflow-hidden">
            <img 
              src="/api/placeholder/400/500" 
              alt="Video preview" 
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/50 to-transparent">
              <div className="flex items-center justify-between text-white">
                <div className="flex items-center space-x-2">
                  <Play className="w-4 h-4" />
                  <span className="text-xs">0:00 / 0:26</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Volume2 className="w-4 h-4" />
                  <Maximize2 className="w-4 h-4" />
                  <MoreVertical className="w-4 h-4" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Second Video */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="relative aspect-[4/5] bg-gray-100 rounded-xl overflow-hidden">
            <img 
              src="/api/placeholder/400/500" 
              alt="Video preview" 
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/50 to-transparent">
              <div className="flex items-center justify-between text-white">
                <div className="flex items-center space-x-2">
                  <Play className="w-4 h-4" />
                  <span className="text-xs">0:00 / 0:20</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Volume2 className="w-4 h-4" />
                  <Maximize2 className="w-4 h-4" />
                  <MoreVertical className="w-4 h-4" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextToVideo;