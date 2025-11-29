'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import AnalysisForm from '@/components/AnalysisForm'
import ResultsDashboard from '@/components/ResultsDashboard'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import CardanoLogo from '@/components/CardanoLogo'
import { Sparkles, Zap, Shield, Globe, Rocket } from 'lucide-react'

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showFloatingButton, setShowFloatingButton] = useState(false)

  const handleAnalysisComplete = (result: any) => {
    console.log('✅ Analysis complete - updating UI')
    setAnalysisResult(result)
    setIsLoading(false)
  }

  const handleNewAnalysis = () => {
    setAnalysisResult(null)
  }

  const scrollToForm = () => {
    document.getElementById('analysis-form')?.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    })
  }

  useEffect(() => {
    const handleScroll = () => {
      const formElement = document.getElementById('analysis-form')
      if (formElement && !analysisResult) {
        const rect = formElement.getBoundingClientRect()
        // Show floating button when form is not visible in viewport
        setShowFloatingButton(rect.top < -100 || rect.bottom > window.innerHeight + 100)
      } else {
        setShowFloatingButton(false)
      }
    }

    window.addEventListener('scroll', handleScroll)
    handleScroll() // Check initial state

    return () => window.removeEventListener('scroll', handleScroll)
  }, [analysisResult])

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Cardano-themed background elements */}
      <div className="fixed inset-0 pointer-events-none">
        {/* Floating Cardano logos */}
        <motion.div
          animate={{
            y: [0, -20, 0],
            opacity: [0.05, 0.1, 0.05]
          }}
          transition={{ duration: 8, repeat: Infinity }}
          className="absolute top-20 left-10 text-blue-500"
        >
          <CardanoLogo className="w-32 h-32" />
        </motion.div>
        <motion.div
          animate={{
            y: [0, 20, 0],
            opacity: [0.05, 0.1, 0.05]
          }}
          transition={{ duration: 10, repeat: Infinity, delay: 2 }}
          className="absolute bottom-40 right-20 text-purple-500"
        >
          <CardanoLogo className="w-32 h-32" />
        </motion.div>

        {/* Blockchain hexagon pattern */}
        <div className="absolute top-1/4 right-1/4 text-6xl text-purple-500/5">
          ⬢⬢⬢<br />⬢⬢⬢<br />⬢⬢⬢
        </div>
      </div>

      <div className="scanlines fixed inset-0 z-50 pointer-events-none" />
      <Header />

      {/* Floating Start Analysis Button */}
      <AnimatePresence>
        {showFloatingButton && !analysisResult && (
          <motion.button
            initial={{ opacity: 0, y: 100, scale: 0 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 100, scale: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 20 }}
            onClick={scrollToForm}
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9 }}
            className="fixed bottom-8 right-8 z-40 pixel-card px-6 py-4 bg-gradient-to-r from-green-600 to-blue-600 border-green-400 hover:from-green-500 hover:to-blue-500 transition-all duration-200 shadow-2xl group"
            style={{ boxShadow: '8px 8px 0px 0px rgba(0, 0, 0, 0.8)' }}
          >
            <div className="absolute inset-0 blockchain-flow opacity-70" />
            <div className="relative z-10 flex items-center gap-3">
              <motion.div
                animate={{ 
                  rotate: [0, 360],
                  scale: [1, 1.2, 1]
                }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Rocket className="w-6 h-6 text-white" />
              </motion.div>
              <div className="text-left">
                <div className="font-press-start text-xs text-white leading-relaxed">
                  START
                </div>
                <div className="font-press-start text-xs text-green-200 leading-relaxed">
                  ANALYSIS
                </div>
              </div>
            </div>
            {/* Animated corners */}
            <motion.div 
              className="absolute top-0 left-0 w-3 h-3 bg-white"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
            />
            <motion.div 
              className="absolute top-0 right-0 w-3 h-3 bg-white"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: 0.375 }}
            />
            <motion.div 
              className="absolute bottom-0 left-0 w-3 h-3 bg-white"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: 0.75 }}
            />
            <motion.div 
              className="absolute bottom-0 right-0 w-3 h-3 bg-white"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: 1.125 }}
            />
          </motion.button>
        )}
      </AnimatePresence>

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 max-w-6xl relative z-10">
        {!analysisResult ? (
          <div className="space-y-20">
            {/* Hero Section with Cardano + Masumi Branding */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto text-center space-y-8"
            >
              {/* Powered by badges */}
              <div className="flex items-center justify-center gap-4 flex-wrap">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: 'spring' }}
                  className="pixel-card px-6 py-3 bg-blue-900/50 border-blue-500 inline-flex items-center gap-3"
                >
                  <CardanoLogo className="w-8 h-8 text-blue-400" />
                  <div className="text-left">
                    <div className="font-press-start text-xs text-blue-400">POWERED BY</div>
                    <div className="font-vt323 text-xl text-blue-300">CARDANO</div>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                  className="pixel-card px-6 py-3 bg-purple-900/50 border-purple-500 inline-flex items-center gap-3"
                >
                  <span className="text-3xl">⬢</span>
                  <div className="text-left">
                    <div className="font-press-start text-xs text-purple-400">SECURED BY</div>
                    <div className="font-vt323 text-xl text-purple-300">MASUMI NETWORK</div>
                  </div>
                </motion.div>
              </div>

              {/* System Ready Badge */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="inline-block border-4 border-green-500 bg-black px-6 py-3 mb-4 relative overflow-hidden"
              >
                <div className="absolute inset-0 blockchain-flow opacity-50" />
                <span className="text-neon-green font-press-start text-sm relative z-10 flex items-center gap-3">
                  <span className="animate-pulse">●</span>
                  BLOCKCHAIN TERMINAL READY // INSERT TOKEN
                </span>
              </motion.div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight animate-glitch">
                <motion.span
                  className="block mb-4"
                  animate={{ textShadow: ['0 0 10px #8b5cf6', '0 0 20px #8b5cf6', '0 0 10px #8b5cf6'] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  LAUNCH YOUR TOKEN
                </motion.span>
                <span className="text-neon-pink block">TO THE MOON</span>
                <motion.span
                  className="block text-2xl text-blue-400 mt-4 font-vt323"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.6 }}
                >
                  ON CARDANO BLOCKCHAIN
                </motion.span>
              </h1>
            </motion.div>

            {/* Features Grid */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8"
            >
              <FeatureCard
                icon={<Zap className="w-8 h-8 text-yellow-400" />}
                title="READINESS SCORE"
                description="AI-POWERED ANALYSIS"
                badge={<CardanoLogo className="w-6 h-6" />}
                color="yellow"
              />
              <FeatureCard
                icon={<Globe className="w-8 h-8 text-blue-400" />}
                title="AUTO PROPOSALS"
                description="EXCHANGE-READY DOCS"
                badge={<span className="text-2xl">⬢</span>}
                color="blue"
              />
              <FeatureCard
                icon={<Sparkles className="w-8 h-8 text-purple-400" />}
                title="BRIDGE ROUTES"
                description="CROSS-CHAIN PATHS"
                badge={<CardanoLogo className="w-6 h-6" />}
                color="purple"
              />
              <FeatureCard
                icon={<Shield className="w-8 h-8 text-green-400" />}
                title="MASUMI AUDIT"
                description="ON-CHAIN LOGGING"
                badge={<span className="text-2xl">⬢</span>}
                color="green"
              />
            </motion.div>

            {/* Analysis Form */}
            <motion.div
              id="analysis-form"
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
              className="max-w-3xl mx-auto"
            >
              <AnalysisForm
                onAnalysisComplete={handleAnalysisComplete}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            </motion.div>
          </div>
        ) : (
          <ResultsDashboard
            result={analysisResult}
            onNewAnalysis={handleNewAnalysis}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}

function FeatureCard({ icon, title, description, badge, color }: {
  icon: React.ReactNode
  title: string
  description: string
  badge: React.ReactNode
  color: string
}) {
  const colorMap: Record<string, string> = {
    yellow: 'border-yellow-500 hover:border-yellow-400',
    blue: 'border-blue-500 hover:border-blue-400',
    purple: 'border-purple-500 hover:border-purple-400',
    green: 'border-green-500 hover:border-green-400'
  }

  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      className={`pixel-card p-6 transition-all duration-200 group ${colorMap[color]}`}
    >
      {/* Blockchain badge */}
      <div className="absolute -top-3 -right-3 w-10 h-10 bg-slate-900 border-4 border-purple-500 flex items-center justify-center rotate-12 group-hover:rotate-0 transition-transform">
        {badge}
      </div>

      <div className="mb-4 border-4 border-slate-700 w-16 h-16 flex items-center justify-center bg-black group-hover:bg-slate-800 transition-colors relative overflow-hidden">
        <div className="absolute inset-0 blockchain-flow opacity-0 group-hover:opacity-30" />
        <div className="relative z-10">{icon}</div>
      </div>
      <h3 className="text-sm text-white mb-2 font-press-start leading-relaxed">{title}</h3>
      <p className="text-slate-400 text-lg font-vt323 leading-none">{description}</p>
    </motion.div>
  )
}
