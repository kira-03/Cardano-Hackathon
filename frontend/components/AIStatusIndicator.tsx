'use client'

import { useEffect, useState } from 'react'

export default function AIStatusIndicator() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Show after component mounts
    const timer = setTimeout(() => setIsVisible(true), 500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div 
      className={`fixed bottom-6 right-6 z-50 transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-3 rounded-full shadow-2xl flex items-center gap-3 border-2 border-white">
        <div className="relative">
          <span className="text-2xl">🤖</span>
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse"></span>
        </div>
        <div className="text-left">
          <div className="text-xs font-bold">AI ANALYSIS ACTIVE</div>
          <div className="text-xs opacity-90">Powered by Gemini 2.5 Flash</div>
        </div>
      </div>
    </div>
  )
}
