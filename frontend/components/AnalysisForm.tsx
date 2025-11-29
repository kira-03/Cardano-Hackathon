'use client'

import { useState } from 'react'
import axios from 'axios'

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

    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/analyze`, {
        policy_id: policyId.trim(),
        target_exchanges: targetExchanges,
        target_chains: targetChains
      })

      onAnalysisComplete(response.data)
    } catch (err: any) {
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
    <div className="bg-white border border-slate-200 rounded-lg p-8">
      <h2 className="text-2xl font-semibold text-slate-900 mb-6">Start Analysis</h2>
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Policy ID Input */}
        <div>
          <label htmlFor="policyId" className="block text-sm font-semibold text-slate-700 mb-2">
            Policy ID
          </label>
          <input
            type="text"
            id="policyId"
            value={policyId}
            onChange={(e) => setPolicyId(e.target.value)}
            placeholder="29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c6"
            className="w-full px-4 py-3 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
            disabled={isLoading}
          />
          <p className="mt-2 text-sm text-slate-500">
            Your Cardano native token policy ID
          </p>
        </div>

        {/* Target Exchanges */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-3">
            Target Exchanges
          </label>
          <div className="grid grid-cols-2 gap-3">
            {exchanges.map(exchange => (
              <button
                key={exchange}
                type="button"
                onClick={() => toggleExchange(exchange)}
                className={`px-4 py-3 rounded-md border font-medium transition-all ${
                  targetExchanges.includes(exchange)
                    ? 'border-blue-600 bg-blue-600 text-white shadow-sm'
                    : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'
                }`}
                disabled={isLoading}
              >
                {exchange}
              </button>
            ))}
          </div>
        </div>

        {/* Target Chains */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-3">
            Target Chains
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {chains.map(chain => (
              <button
                key={chain}
                type="button"
                onClick={() => toggleChain(chain)}
                className={`px-4 py-3 rounded-md border font-medium transition-all ${
                  targetChains.includes(chain)
                    ? 'border-blue-600 bg-blue-600 text-white shadow-sm'
                    : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'
                }`}
                disabled={isLoading}
              >
                {chain}
              </button>
            ))}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-800 px-4 py-3 text-sm">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !policyId.trim()}
          className="w-full bg-blue-600 text-white py-4 px-6 rounded-md font-semibold hover:bg-blue-700 transition-colors disabled:bg-slate-300 disabled:cursor-not-allowed disabled:text-slate-500 shadow-sm"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Token...
            </span>
          ) : (
            'Start Analysis'
          )}
        </button>
      </form>

      {/* Example Policy IDs */}
      <div className="mt-8 pt-6 border-t border-slate-200">
        <p className="text-sm text-slate-600 mb-3">Need a test token?</p>
        <button
          onClick={() => setPolicyId('29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c6')}
          className="text-sm px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-md text-slate-700 font-mono transition-colors"
          disabled={isLoading}
        >
          Use example policy ID
        </button>
      </div>
    </div>
  )
}
