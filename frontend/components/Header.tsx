'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

export default function Header() {
  const [blockHeight, setBlockHeight] = useState(8234567)
  const [currentHash, setCurrentHash] = useState('')

  useEffect(() => {
    // Initialize hash on client side only
    setCurrentHash(generateHash())

    // Update block height every 5 seconds
    const blockInterval = setInterval(() => {
      setBlockHeight(prev => prev + 1)
    }, 5000)

    // Update hash every 1.5 seconds
    const hashInterval = setInterval(() => {
      setCurrentHash(generateHash())
    }, 1500)

    return () => {
      clearInterval(blockInterval)
      clearInterval(hashInterval)
    }
  }, [])

  const generateHash = () => {
    return `0x${Math.random().toString(16).substring(2, 34)}...${Math.random().toString(16).substring(2, 10)}`
  }

  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 border-b-4 border-purple-500 backdrop-blur-sm relative overflow-hidden">
      {/* Blockchain flow animation */}
      <div className="absolute inset-0 blockchain-flow opacity-30" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 max-w-6xl relative z-10">
        <div className="flex items-center justify-between flex-wrap gap-4">
          {/* Logo & Brand */}
          <div className="flex items-center gap-4">
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 bg-purple-600 border-4 border-purple-400 flex items-center justify-center shadow-[4px_4px_0px_0px_#4c1d95] relative"
            >
              <span className="text-2xl">⬢</span>
              <div className="absolute inset-0 border-2 border-purple-300 opacity-50" style={{ margin: '4px' }} />
            </motion.div>
            <div>
              <h1 className="text-xl font-press-start text-white tracking-widest">NAVIGATOR</h1>
              <p className="font-vt323 text-sm text-purple-400">BLOCKCHAIN ANALYSIS TERMINAL</p>
            </div>
          </div>

          {/* Blockchain Stats */}
          <div className="flex items-center gap-3">
            {/* Block Height */}
            <motion.div
              className="hidden md:flex items-center gap-3 px-4 py-3 bg-slate-800/80 border-4 border-purple-500 relative overflow-hidden"
              animate={{ 
                borderColor: ['#a855f7', '#8b5cf6', '#a855f7'],
                boxShadow: [
                  '4px 4px 0px 0px rgba(0,0,0,0.5)',
                  '6px 6px 0px 0px rgba(0,0,0,0.5)',
                  '4px 4px 0px 0px rgba(0,0,0,0.5)'
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="absolute inset-0 blockchain-flow opacity-20" />
              <motion.span 
                className="text-purple-400 text-2xl relative z-10"
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
              >
                ⬢
              </motion.span>
              <div className="relative z-10">
                <div className="font-press-start text-[9px] text-purple-400 leading-tight">BLOCK</div>
                <div className="font-vt323 text-lg text-purple-200 leading-none mt-1">{blockHeight.toLocaleString()}</div>
              </div>
            </motion.div>

            {/* Network Status */}
            <motion.div 
              className="hidden sm:flex items-center gap-3 px-4 py-3 bg-slate-800/80 border-4 border-green-500 relative overflow-hidden"
              style={{ boxShadow: '4px 4px 0px 0px rgba(0,0,0,0.5)' }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-green-900/30 to-emerald-900/30" />
              <motion.div
                className="w-3 h-3 bg-green-400 relative z-10"
                animate={{ 
                  opacity: [1, 0.3, 1],
                  boxShadow: [
                    '0 0 0px rgba(74, 222, 128, 0)',
                    '0 0 10px rgba(74, 222, 128, 1)',
                    '0 0 0px rgba(74, 222, 128, 0)'
                  ]
                }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <span className="font-press-start text-[9px] text-green-300 relative z-10 leading-tight">
                ONLINE
              </span>
            </motion.div>

            {/* API Docs Button */}
            <motion.a
              href="http://localhost:8000/docs"
              target="_blank"
              className="pixel-card px-4 py-3 bg-blue-900/50 border-blue-500 hover:bg-blue-800/50 transition-all flex items-center gap-2 relative overflow-hidden group"
              style={{ boxShadow: '4px 4px 0px 0px rgba(0,0,0,0.5)' }}
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="absolute inset-0 blockchain-flow opacity-0 group-hover:opacity-30 transition-opacity" />
              <span className="text-xl relative z-10">📡</span>
              <span className="hidden sm:inline font-press-start text-[9px] text-blue-300 relative z-10">API</span>
            </motion.a>
          </div>
        </div>

        {/* Hash Display */}
        {currentHash && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 px-3 py-2 bg-black/50 border-l-4 border-purple-500 overflow-hidden"
          >
            <div className="flex items-center gap-2">
              <span className="font-press-start text-[8px] text-purple-400">LATEST HASH:</span>
              <motion.span
                key={currentHash}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="font-mono text-xs text-green-400 truncate"
              >
                {currentHash}
              </motion.span>
            </div>
          </motion.div>
        )}
      </div>
    </header>
  )
}
