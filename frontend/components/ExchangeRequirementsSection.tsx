import { motion } from 'framer-motion'

interface ExchangeRequirement {
  exchange: string
  requirement: string
  current_status: string
  meets_requirement: boolean
}

interface ExchangeRequirementsSectionProps {
  requirements: ExchangeRequirement[]
  proposalUrl?: string | null
}

export default function ExchangeRequirementsSection({ requirements, proposalUrl }: ExchangeRequirementsSectionProps) {
  const groupedRequirements = requirements.reduce((acc, req) => {
    if (!acc[req.exchange]) {
      acc[req.exchange] = []
    }
    acc[req.exchange].push(req)
    return acc
  }, {} as Record<string, ExchangeRequirement[]>)

  const getComplianceRate = (reqs: ExchangeRequirement[]) => {
    const met = reqs.filter(r => r.meets_requirement).length
    return Math.round((met / reqs.length) * 100)
  }

  const getComplianceColor = (rate: number) => {
    if (rate >= 80) return { bg: 'bg-green-600', border: 'border-green-400' }
    if (rate >= 50) return { bg: 'bg-yellow-600', border: 'border-yellow-400' }
    return { bg: 'bg-red-600', border: 'border-red-400' }
  }

  const exchangeIcons: Record<string, string> = {
    'Binance': '🟡',
    'KuCoin': '🟢',
    'Gate.io': '🔵',
    'MEXC': '🟣',
    'default': '🏦'
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-press-start text-lg text-white flex items-center gap-3">
          <span className="text-2xl">🏦</span>
          EXCHANGE REQUIREMENTS
        </h3>
        {proposalUrl && (
          <button
            onClick={() => window.open(proposalUrl, '_blank')}
            className="pixel-btn pixel-btn-primary flex items-center gap-2"
          >
            <span className="text-xl">📄</span>
            VIEW PROPOSAL
          </button>
        )}
      </div>

      <div className="space-y-5">
        {Object.entries(groupedRequirements).map(([exchange, reqs], idx) => {
          const complianceRate = getComplianceRate(reqs)
          const metCount = reqs.filter(r => r.meets_requirement).length
          const colors = getComplianceColor(complianceRate)

          return (
            <motion.div
              key={exchange}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-slate-900/50 border-4 border-slate-700"
            >
              {/* Exchange Header */}
              <div className="px-6 py-5 bg-slate-800/50 border-b-4 border-slate-700">
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div className="flex items-center gap-4">
                    <span className="text-4xl">{exchangeIcons[exchange] || exchangeIcons.default}</span>
                    <div>
                      <h4 className="font-press-start text-sm text-white mb-1">{exchange}</h4>
                      <span className="font-vt323 text-lg text-slate-400">
                        {metCount} OF {reqs.length} REQUIREMENTS MET
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {/* Progress Bar */}
                    <div className="w-32 h-6 bg-black border-2 border-slate-700 relative overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${complianceRate}%` }}
                        transition={{ delay: 0.3 + idx * 0.1, duration: 0.8 }}
                        className={`h-full ${colors.bg}`}
                      />
                    </div>
                    <div className={`${colors.bg} ${colors.border} border-2 px-4 py-2 min-w-[4rem] text-center`}>
                      <span className="font-press-start text-sm text-white">
                        {complianceRate}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Requirements List */}
              <div className="divide-y-2 divide-slate-700">
                {reqs.map((req, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 + index * 0.05 }}
                    className="px-6 py-4 hover:bg-slate-800/30 transition-colors"
                  >
                    <div className="flex items-start gap-4">
                      <div className={`flex-shrink-0 w-8 h-8 border-2 flex items-center justify-center ${req.meets_requirement
                          ? 'bg-green-600 border-green-400'
                          : 'bg-red-600 border-red-400'
                        }`}>
                        <span className="text-white text-xl">
                          {req.meets_requirement ? '✓' : '✗'}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-press-start text-xs text-white mb-2">{req.requirement}</p>
                        <p className="font-vt323 text-lg text-slate-400">{req.current_status}</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
