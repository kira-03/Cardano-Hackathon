import { motion } from 'framer-motion'

interface BridgeRoute {
  source_chain: string
  target_chain: string
  bridge_name: string
  estimated_fee: string
  estimated_time: string
  trust_model: string
  slippage_estimate: string
  hops: number
  recommendation_score: number
}

interface BridgeRoutesSectionProps {
  routes: BridgeRoute[]
  recommendedChain: string
}

export default function BridgeRoutesSection({ routes, recommendedChain }: BridgeRoutesSectionProps) {
  const getTrustModelStyles = (model: string) => {
    const styles: Record<string, { bg: string; border: string }> = {
      trustless: { bg: 'bg-green-600', border: 'border-green-400' },
      hybrid: { bg: 'bg-blue-600', border: 'border-blue-400' },
      custodial: { bg: 'bg-yellow-600', border: 'border-yellow-400' }
    }
    return styles[model.toLowerCase()] || styles.hybrid
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return { bg: 'bg-green-600', border: 'border-green-400' }
    if (score >= 60) return { bg: 'bg-blue-600', border: 'border-blue-400' }
    if (score >= 40) return { bg: 'bg-yellow-600', border: 'border-yellow-400' }
    return { bg: 'bg-red-600', border: 'border-red-400' }
  }

  const chainIcons: Record<string, string> = {
    'Ethereum': '⟠',
    'BSC': '🟡',
    'Polygon': '🟣',
    'Solana': '🌐',
    'Avalanche': '🔺',
    'default': '🌉'
  }

  const groupedRoutes = routes.reduce((acc, route) => {
    if (!acc[route.target_chain]) {
      acc[route.target_chain] = []
    }
    acc[route.target_chain].push(route)
    return acc
  }, {} as Record<string, BridgeRoute[]>)

  Object.keys(groupedRoutes).forEach(chain => {
    groupedRoutes[chain].sort((a, b) => b.recommendation_score - a.recommendation_score)
  })

  return (
    <div>
      <div className="mb-6">
        <h3 className="font-press-start text-lg text-white mb-6 flex items-center gap-3">
          <span className="text-2xl">🌉</span>
          CROSS-CHAIN BRIDGE ROUTES
        </h3>
        {recommendedChain && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-4 p-5 bg-blue-900/50 border-4 border-blue-500"
          >
            <div className="w-14 h-14 bg-blue-600 border-4 border-blue-400 flex items-center justify-center">
              <span className="text-3xl">⭐</span>
            </div>
            <div>
              <p className="font-press-start text-xs text-blue-400 mb-1">RECOMMENDED CHAIN</p>
              <p className="font-vt323 text-xl text-blue-200">
                <span className="text-white font-bold">{recommendedChain}</span> OFFERS THE BEST BALANCE FOR CROSS-CHAIN EXPANSION
              </p>
            </div>
          </motion.div>
        )}
      </div>

      <div className="space-y-5">
        {Object.entries(groupedRoutes).map(([chain, chainRoutes], idx) => (
          <motion.div
            key={chain}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className={`bg-slate-900/50 border-4 ${chain === recommendedChain ? 'border-blue-500' : 'border-slate-700'
              }`}
          >
            {/* Chain Header */}
            <div className={`px-6 py-4 border-b-4 ${chain === recommendedChain
                ? 'bg-blue-900/50 border-blue-700'
                : 'bg-slate-800/50 border-slate-700'
              }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-4xl">{chainIcons[chain] || chainIcons.default}</span>
                  <div>
                    <h4 className="font-press-start text-sm text-white flex items-center gap-2">
                      {chain === recommendedChain && <span className="text-yellow-400">★</span>}
                      CARDANO → {chain.toUpperCase()}
                    </h4>
                    <span className="font-vt323 text-lg text-slate-400">
                      {chainRoutes.length} BRIDGE{chainRoutes.length !== 1 ? 'S' : ''} AVAILABLE
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Routes List */}
            <div className="divide-y-2 divide-slate-700">
              {chainRoutes.map((route, index) => {
                const scoreColors = getScoreColor(route.recommendation_score)
                const trustColors = getTrustModelStyles(route.trust_model)

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="p-6 hover:bg-slate-800/30 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-5 flex-wrap gap-4">
                      <div>
                        <div className="flex items-center gap-3 mb-3">
                          <h5 className="font-press-start text-sm text-white">{route.bridge_name}</h5>
                          {index === 0 && chainRoutes.length > 1 && (
                            <span className="pixel-tag bg-blue-600 border-blue-400 text-white text-xs">
                              RECOMMENDED
                            </span>
                          )}
                        </div>
                        <span className={`${trustColors.bg} ${trustColors.border} border-2 px-3 py-1 font-press-start text-xs text-white uppercase inline-block`}>
                          {route.trust_model}
                        </span>
                      </div>
                      <div className={`${scoreColors.bg} ${scoreColors.border} border-4 px-6 py-3 text-center min-w-[5rem]`}>
                        <div className="font-press-start text-2xl text-white">
                          {route.recommendation_score}
                        </div>
                        <div className="font-vt323 text-sm text-white/80">SCORE</div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                        <p className="font-press-start text-[10px] text-slate-500 mb-2">FEE</p>
                        <p className="font-vt323 text-xl text-white">{route.estimated_fee}</p>
                      </div>
                      <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                        <p className="font-press-start text-[10px] text-slate-500 mb-2">TIME</p>
                        <p className="font-vt323 text-xl text-white">{route.estimated_time}</p>
                      </div>
                      <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                        <p className="font-press-start text-[10px] text-slate-500 mb-2">SLIPPAGE</p>
                        <p className="font-vt323 text-xl text-white">{route.slippage_estimate}</p>
                      </div>
                      <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                        <p className="font-press-start text-[10px] text-slate-500 mb-2">HOPS</p>
                        <p className="font-vt323 text-xl text-white">{route.hops}</p>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
