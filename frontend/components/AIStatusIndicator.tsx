'use client'

import { useEffect, useState } from 'react'
// Removed AISymbol import

export default function AIStatusIndicator() {
  const [isVisible, setIsVisible] = useState(false)
  const [isDismissed, setIsDismissed] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 800)
    const hideTimer = setTimeout(() => setIsDismissed(true), 8000)
    return () => {
      clearTimeout(timer)
      clearTimeout(hideTimer)
    }
  }, [])

  if (isDismissed) return null

  return (
    <div 
      className={`fixed bottom-6 right-6 z-50 transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <div className="bg-white text-slate-700 pl-4 pr-3 py-3 rounded-2xl shadow-lg border border-slate-200 flex items-center gap-3">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
          <span className="text-sm font-medium">AI Ready</span>
        </div>
        <span className="text-xs text-slate-400 flex items-center gap-1">
          <span className="text-base">👾</span>
          OpenAI GPT-4.1
        </span>
        <button 
          onClick={() => setIsDismissed(true)}
          className="p-1 hover:bg-slate-100 rounded-lg transition-colors"
        >
          <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  )
}
