import React from 'react';

const FooterSection = () => {
  const handleSubscribe = (e) => {
    e.preventDefault();
    // Handle subscription
  };

  return (
    <footer className="max-w-7xl mx-auto px-8 py-20">
      {/* Logo and Newsletter */}
      <div className="mb-20">
        <div className="text-left">
          <h2 className="text-2xl font-bold mb-8 text-left">Luga AI</h2>
        </div>
        <form onSubmit={handleSubscribe} className="flex gap-4 max-w-md">
          <input
            type="email"
            placeholder="name@email.com"
            className="flex-1 p-3 rounded-full bg-gray-50"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-gray-900 text-white rounded-full hover:bg-gray-800 transition-colors"
          >
            Subscribe
          </button>
        </form>
      </div>

      {/* Navigation Links */}
      <div className="flex gap-24 mb-20">
        {/* Product Column */}
        <div>
          <h3 className="text-xl font-medium mb-6">Product</h3>
          <ul className="space-y-4 text-left">
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Features</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Pricing</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Roadmap</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">About</a></li>
          </ul>
        </div>

        {/* Support Column */}
        <div>
          <h3 className="text-xl font-medium mb-6">Support</h3>
          <ul className="space-y-4 text-left">
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Help Desk</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Public roadmap</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Discord</a></li>
          </ul>
        </div>

        {/* Company Column */}
        <div>
          <h3 className="text-xl font-medium mb-6">Company</h3>
          <ul className="space-y-4 text-left">
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Privacy Policy</a></li>
            <li><a href="#" className="text-gray-600 hover:text-gray-900">Terms of use</a></li>
          </ul>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="flex justify-between items-center pt-8 border-t border-gray-200">
        <p className="text-gray-600">
          Luga AI. All right reserved. © 2024
        </p>
        <div className="flex gap-6">
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
            <img 
              src="/twitter.png" 
              alt="Twitter" 
              className="w-5 h-5 opacity-50 hover:opacity-75 transition-opacity"
            />
          </a>
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
            <img 
              src="/facebook.png" 
              alt="Facebook" 
              className="w-5 h-5 opacity-50 hover:opacity-75 transition-opacity"
            />
          </a>
          <a href="https://youtube.com" target="_blank" rel="noopener noreferrer">
            <img 
              src="/youtube.png" 
              alt="YouTube" 
              className="w-5 h-5 opacity-50 hover:opacity-75 transition-opacity"
            />
          </a>
        </div>
      </div>
    </footer>
  );
};

export default FooterSection;