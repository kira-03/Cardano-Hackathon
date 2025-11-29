interface MasumiLog {
  agent_did: string
  decision_type: string
  decision_hash: string
  transaction_id?: string | null
  timestamp: string
}

interface MasumiLogsSectionProps {
  logs: MasumiLog[]
}

export default function MasumiLogsSection({ logs }: MasumiLogsSectionProps) {
  const getDecisionTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      token_analysis: '📊',
      exchange_preparation: '📋',
      cross_chain_routing: '🌉',
      pdf_generation: '📄'
    }
    return icons[type] || '📝'
  }

  const getDecisionTypeLabel = (type: string) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ')
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  const truncateHash = (hash: string) => {
    if (hash.length <= 20) return hash
    return `${hash.slice(0, 10)}...${hash.slice(-10)}`
  }

  return (
    <div>
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Masumi Network Audit Log</h3>
        <p className="text-sm text-gray-600">
          All agent decisions are cryptographically logged on the Cardano blockchain via Masumi Network for auditability and transparency.
        </p>
      </div>

      {/* Agent DID */}
      {logs.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <span className="text-2xl mr-3">🔐</span>
            <div>
              <p className="text-sm font-medium text-blue-900">Agent Decentralized Identifier (DID)</p>
              <p className="text-xs text-blue-700 font-mono mt-1">{logs[0].agent_did}</p>
            </div>
          </div>
        </div>
      )}

      {/* Logs Timeline */}
      <div className="space-y-4">
        {logs.map((log, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
            <div className="flex items-start">
              {/* Icon */}
              <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-cardano-blue to-indigo-600 rounded-lg flex items-center justify-center text-2xl">
                {getDecisionTypeIcon(log.decision_type)}
              </div>

              {/* Content */}
              <div className="ml-4 flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-lg font-semibold text-gray-900">
                    {getDecisionTypeLabel(log.decision_type)}
                  </h4>
                  <span className="text-xs text-gray-500">{formatTimestamp(log.timestamp)}</span>
                </div>

                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Decision Hash</p>
                    <p className="text-sm font-mono text-gray-700 bg-gray-50 px-2 py-1 rounded">
                      {truncateHash(log.decision_hash)}
                    </p>
                  </div>

                  {log.transaction_id && (
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Blockchain Transaction</p>
                      <div className="flex items-center">
                        <p className="text-sm font-mono text-gray-700 bg-gray-50 px-2 py-1 rounded flex-1">
                          {truncateHash(log.transaction_id)}
                        </p>
                        {log.transaction_id.startsWith('mock_') ? (
                          <span className="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                            Simulated
                          </span>
                        ) : (
                          <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                            On-Chain
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Checkmark */}
              <div className="flex-shrink-0 ml-4">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 text-lg">✓</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Info Footer */}
      <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-start">
          <span className="text-xl mr-3">ℹ️</span>
          <div>
            <p className="text-sm font-medium text-gray-900 mb-1">About Masumi Network Logging</p>
            <p className="text-xs text-gray-600">
              Masumi Network provides decentralized identity and decision logging for AI agents on Cardano. 
              Each decision is cryptographically hashed and recorded on-chain, creating an immutable audit trail 
              that ensures transparency and accountability for all agent actions.
            </p>
            <a 
              href="https://docs.masumi.network" 
              target="_blank" 
              className="text-xs text-cardano-blue hover:underline mt-2 inline-block"
            >
              Learn more about Masumi Network →
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
