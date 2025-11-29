'use client'

import { useState } from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { Sparkles, TrendingUp, AlertCircle, ArrowRight, Zap } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface AnalysisFormProps {
  onAnalysisComplete: (result: any) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export default function AnalysisForm({ onAnalysisComplete, isLoading, setIsLoading }: AnalysisFormProps) {
  const [policyId, setPolicyId] = useState('')
  const [targetExchanges, setTargetExchanges] = useState<string[]>(['Binance', 'KuCoin'])
  const [targetChains, setTargetChains] = useState<string[]>(['Ethereum', 'BSC'])
  const [error, setError] = useState('')

  const exchanges = ['Binance', 'KuCoin', 'Gate.io', 'MEXC']
  const chains = ['Ethereum', 'BSC', 'Polygon', 'Solana', 'Avalanche']

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!policyId.trim()) {
      setError('Please enter a policy ID')
      return
    }

    console.log('🚀 Starting token analysis...')
    console.log('📋 Policy ID:', policyId.trim())
    console.log('🏦 Target Exchanges:', targetExchanges)
    console.log('⛓️ Target Chains:', targetChains)
    console.log('🔗 API URL:', API_URL)

    setIsLoading(true)

    try {
      console.log('📡 Sending POST request to:', `${API_URL}/api/analyze`)
      const startTime = Date.now()

      const response = await axios.post(`${API_URL}/api/analyze`, {
        policy_id: policyId.trim(),
        target_exchanges: targetExchanges,
        target_chains: targetChains
      })

      const duration = Date.now() - startTime
      console.log(`✅ Analysis complete in ${duration}ms`)
      console.log('📊 Response data:', response.data)
      console.log('🎯 Token:', response.data.token_name, '(' + response.data.token_symbol + ')')
      console.log('⭐ Grade:', response.data.readiness_score.grade, '- Score:', response.data.readiness_score.total_score)
      console.log('💡 Recommendations:', response.data.recommendations.length)

      onAnalysisComplete(response.data)
    } catch (err: any) {
      console.error('❌ Analysis failed')
      console.error('Error details:', err)
      console.error('Response status:', err.response?.status)
      console.error('Response data:', err.response?.data)
      console.error('Error message:', err.message)

      setError(err.response?.data?.detail || 'Analysis failed. Please check your policy ID and try again.')
      setIsLoading(false)
    }
  }

  const toggleExchange = (exchange: string) => {
    setTargetExchanges(prev =>
      prev.includes(exchange)
        ? prev.filter(e => e !== exchange)
        : [...prev, exchange]
    )
  }

  const toggleChain = (chain: string) => {
    setTargetChains(prev =>
      prev.includes(chain)
        ? prev.filter(c => c !== chain)
        : [...prev, chain]
    )
  }

  return (
    <div className="pixel-card p-8 relative">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8 relative z-10"
      >
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-5 h-5 text-yellow-400" />
          <h2 className="text-xl text-white font-press-start">START ANALYSIS</h2>
        </div>
        <p className="text-sm text-slate-400 font-vt323 text-xl">ENTER TOKEN COORDINATES FOR ASSESSMENT</p>
      </motion.div>

      <form onSubmit={handleSubmit} className="space-y-8 relative z-10">
        {/* Policy ID Input */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
        >
          <label htmlFor="policyId" className="block text-sm font-press-start text-slate-300 mb-4 flex items-center gap-2">
            <Zap className="w-4 h-4 text-yellow-400" />
            POLICY ID
          </label>
          <motion.input
            type="text"
            id="policyId"
            value={policyId}
            onChange={(e) => setPolicyId(e.target.value)}
            placeholder="29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c6"
            className="pixel-input"
            disabled={isLoading}
            whileFocus={{ scale: 1.01 }}
          />
          <p className="mt-2 text-sm text-slate-500 font-vt323">
            &gt; INPUT CARDANO NATIVE TOKEN POLICY ID
          </p>
        </motion.div>

        {/* Target Exchanges */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          <label className="block text-sm font-press-start text-slate-300 mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-purple-400" />
            TARGET EXCHANGES
          </label>
          <div className="flex flex-wrap gap-3">
            {exchanges.map((exchange, i) => (
              <motion.button
                key={exchange}
                type="button"
                onClick={() => toggleExchange(exchange)}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + i * 0.05 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`pixel-tag transition-all duration-200 ${targetExchanges.includes(exchange)
                    ? 'bg-blue-600 border-blue-400 text-white shadow-[4px_4px_0px_0px_#000033]'
                    : 'bg-slate-800 border-slate-600 text-slate-400 hover:bg-slate-700'
                  }`}
                disabled={isLoading}
              >
                {exchange}
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Target Chains */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <label className="block text-sm font-press-start text-slate-300 mb-4 flex items-center gap-2">
            <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            TARGET CHAINS
          </label>
          <div className="flex flex-wrap gap-3">
            {chains.map((chain, i) => (
              <motion.button
                key={chain}
                type="button"
                onClick={() => toggleChain(chain)}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + i * 0.05 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`pixel-tag transition-all duration-200 ${targetChains.includes(chain)
                    ? 'bg-green-600 border-green-400 text-white shadow-[4px_4px_0px_0px_#003300]'
                    : 'bg-slate-800 border-slate-600 text-slate-400 hover:bg-slate-700'
                  }`}
                disabled={isLoading}
              >
                {chain}
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Error Message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0, marginTop: 0 }}
              animate={{ opacity: 1, height: 'auto', marginTop: 32 }}
              exit={{ opacity: 0, height: 0, marginTop: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="flex items-start gap-3 bg-red-900/50 border-2 border-red-500 text-red-400 px-4 py-3 font-vt323 text-xl">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <span>ERROR: {error}</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={isLoading || !policyId.trim()}
          className="w-full pixel-btn pixel-btn-primary py-4 text-sm relative overflow-hidden"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-3 relative z-10 animate-pulse">
              <Sparkles className="w-5 h-5" />
              PROCESSING...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              INITIATE ANALYSIS
              <ArrowRight className="w-4 h-4" />
            </span>
          )}
        </motion.button>
      </form>

      {/* Example Policy IDs */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="mt-8 pt-6 border-t-2 border-slate-800 relative z-10"
      >
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-500 font-press-start text-[10px]">TEST TOKEN:</p>
          <motion.button
            onClick={() => setPolicyId('279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f')}
            className="text-sm text-blue-400 hover:text-blue-300 font-vt323 text-xl transition-colors flex items-center gap-1"
            disabled={isLoading}
            whileHover={{ x: 5 }}
          >
            LOAD SNEK DATA
            <ArrowRight className="w-3 h-3" />
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}
