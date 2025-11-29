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
  // Group by exchange
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

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-900">Exchange Requirements</h3>
        {proposalUrl && (
          <a 
            href={proposalUrl}
            target="_blank"
            className="px-4 py-2 bg-cardano-blue text-white rounded-lg hover:bg-cardano-dark transition-colors flex items-center"
          >
            <span className="mr-2">📄</span>
            Download Proposal PDF
          </a>
        )}
      </div>

      <div className="space-y-6">
        {Object.entries(groupedRequirements).map(([exchange, reqs]) => {
          const complianceRate = getComplianceRate(reqs)
          
          return (
            <div key={exchange} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              {/* Exchange Header */}
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-semibold text-gray-900">{exchange}</h4>
                  <div className="flex items-center space-x-3">
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${complianceRate >= 80 ? 'text-green-600' : complianceRate >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                        {complianceRate}%
                      </div>
                      <div className="text-xs text-gray-500">Compliance</div>
                    </div>
                    <div className="w-16 h-16">
                      <svg className="transform -rotate-90" width="64" height="64">
                        <circle
                          cx="32"
                          cy="32"
                          r="28"
                          stroke="#e5e7eb"
                          strokeWidth="6"
                          fill="none"
                        />
                        <circle
                          cx="32"
                          cy="32"
                          r="28"
                          stroke={complianceRate >= 80 ? '#10b981' : complianceRate >= 50 ? '#f59e0b' : '#ef4444'}
                          strokeWidth="6"
                          fill="none"
                          strokeDasharray={`${2 * Math.PI * 28}`}
                          strokeDashoffset={`${2 * Math.PI * 28 * (1 - complianceRate / 100)}`}
                          strokeLinecap="round"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              {/* Requirements List */}
              <div className="divide-y divide-gray-200">
                {reqs.map((req, index) => (
                  <div key={index} className="px-6 py-4 hover:bg-gray-50">
                    <div className="flex items-start">
                      <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center ${
                        req.meets_requirement ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        {req.meets_requirement ? (
                          <span className="text-green-600 text-sm">✓</span>
                        ) : (
                          <span className="text-red-600 text-sm">✗</span>
                        )}
                      </div>
                      <div className="ml-3 flex-1">
                        <p className="text-sm font-medium text-gray-900">{req.requirement}</p>
                        <p className="text-xs text-gray-500 mt-1">{req.current_status}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
