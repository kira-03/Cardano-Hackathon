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
  const getTrustModelBadge = (model: string) => {
    const styles = {
      trustless: 'bg-green-100 text-green-800 border-green-200',
      hybrid: 'bg-blue-100 text-blue-800 border-blue-200',
      custodial: 'bg-yellow-100 text-yellow-800 border-yellow-200'
    }
    return styles[model as keyof typeof styles] || styles.hybrid
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-blue-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Group by target chain
  const groupedRoutes = routes.reduce((acc, route) => {
    if (!acc[route.target_chain]) {
      acc[route.target_chain] = []
    }
    acc[route.target_chain].push(route)
    return acc
  }, {} as Record<string, BridgeRoute[]>)

  // Sort routes by recommendation score
  Object.keys(groupedRoutes).forEach(chain => {
    groupedRoutes[chain].sort((a, b) => b.recommendation_score - a.recommendation_score)
  })

  return (
    <div>
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Cross-Chain Bridge Routes</h3>
        {recommendedChain && (
          <div className="bg-cardano-blue bg-opacity-10 border-2 border-cardano-blue rounded-lg p-4">
            <div className="flex items-center">
              <span className="text-2xl mr-3">🌟</span>
              <div>
                <p className="font-semibold text-cardano-blue">Recommended Chain</p>
                <p className="text-gray-700 text-sm">
                  <strong>{recommendedChain}</strong> offers the best balance for your cross-chain expansion
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-6">
        {Object.entries(groupedRoutes).map(([chain, chainRoutes]) => (
          <div key={chain} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            {/* Chain Header */}
            <div className={`px-6 py-4 ${chain === recommendedChain ? 'bg-cardano-blue text-white' : 'bg-gray-50'}`}>
              <div className="flex items-center justify-between">
                <h4 className="text-lg font-semibold flex items-center">
                  {chain === recommendedChain && <span className="mr-2">⭐</span>}
                  Cardano → {chain}
                </h4>
                <span className={`text-sm ${chain === recommendedChain ? 'text-white opacity-90' : 'text-gray-500'}`}>
                  {chainRoutes.length} bridge{chainRoutes.length !== 1 ? 's' : ''} available
                </span>
              </div>
            </div>

            {/* Routes List */}
            <div className="divide-y divide-gray-200">
              {chainRoutes.map((route, index) => (
                <div key={index} className="px-6 py-5 hover:bg-gray-50">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h5 className="text-lg font-semibold text-gray-900">{route.bridge_name}</h5>
                      <span className={`inline-block mt-1 px-2 py-1 rounded-full text-xs font-medium border ${getTrustModelBadge(route.trust_model)}`}>
                        {route.trust_model.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${getScoreColor(route.recommendation_score)}`}>
                        {route.recommendation_score}
                      </div>
                      <div className="text-xs text-gray-500">Score</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-500 text-xs mb-1">Estimated Fee</p>
                      <p className="font-semibold text-gray-900">{route.estimated_fee}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs mb-1">Estimated Time</p>
                      <p className="font-semibold text-gray-900">{route.estimated_time}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs mb-1">Slippage</p>
                      <p className="font-semibold text-gray-900">{route.slippage_estimate}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs mb-1">Hops</p>
                      <p className="font-semibold text-gray-900">{route.hops}</p>
                    </div>
                  </div>

                  {index === 0 && chainRoutes.length > 1 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <span className="text-xs text-green-600 font-medium">✓ Recommended bridge for {chain}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
