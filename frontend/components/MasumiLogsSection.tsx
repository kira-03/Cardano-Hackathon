import { motion } from 'framer-motion'

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
      exchange_preparation: '📝',
      cross_chain_routing: '🌉',
      pdf_generation: '📄'
    }
    return icons[type] || '📋'
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
    if (hash.length <= 16) return hash
    return `${hash.slice(0, 12)}...${hash.slice(-12)}`
  }

  return (
    <div>
      <div className="mb-6">
        <h3 className="font-press-start text-lg text-white mb-4 flex items-center gap-3">
          <span className="text-2xl">📝</span>
          AUDIT LOG
        </h3>
        <p className="font-vt323 text-xl text-slate-400 border-l-4 border-purple-500 pl-4 bg-slate-900/50 p-3">
          AGENT DECISIONS ARE CRYPTOGRAPHICALLY LOGGED ON CARDANO VIA MASUMI NETWORK FOR TRANSPARENCY.
        </p>
      </div>

      {/* Agent DID */}
      {logs.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-4 p-5 bg-purple-900/50 border-4 border-purple-500 mb-6"
        >
          <div className="w-14 h-14 bg-purple-600 border-4 border-purple-400 flex items-center justify-center">
            <span className="text-3xl">🔑</span>
          </div>
          <div className="min-w-0 flex-1">
            <p className="font-press-start text-xs text-purple-400 mb-2">AGENT DID</p>
            <p className="font-vt323 text-lg text-purple-200 font-mono truncate">{logs[0].agent_did}</p>
          </div>
        </motion.div>
      )}

      {/* Logs Timeline */}
      <div className="space-y-4">
        {logs.map((log, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-900/50 border-4 border-slate-700 hover:border-slate-600 transition-colors"
          >
            <div className="flex items-start gap-4 p-5">
              {/* Icon */}
              <div className="w-14 h-14 bg-slate-800 border-2 border-slate-600 flex items-center justify-center flex-shrink-0">
                <span className="text-3xl">{getDecisionTypeIcon(log.decision_type)}</span>
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-4 flex-wrap">
                  <h4 className="font-press-start text-sm text-white">
                    {getDecisionTypeLabel(log.decision_type)}
                  </h4>
                  <span className="font-vt323 text-base text-slate-400 whitespace-nowrap">
                    {formatTimestamp(log.timestamp)}
                  </span>
                </div>

                <div className="grid sm:grid-cols-2 gap-4">
                  <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                    <p className="font-press-start text-[10px] text-slate-500 mb-2">DECISION HASH</p>
                    <p className="font-vt323 text-base text-slate-300 font-mono break-all">
                      {truncateHash(log.decision_hash)}
                    </p>
                  </div>

                  {log.transaction_id && (
                    <div className="bg-slate-800/50 border-2 border-slate-700 p-4">
                      <div className="flex items-center justify-between mb-2">
                        <p className="font-press-start text-[10px] text-slate-500">TRANSACTION</p>
                        {log.transaction_id.startsWith('mock_') ? (
                          <span className="pixel-tag bg-yellow-600 border-yellow-400 text-white text-xs">
                            SIMULATED
                          </span>
                        ) : (
                          <span className="pixel-tag bg-green-600 border-green-400 text-white text-xs">
                            ON-CHAIN
                          </span>
                        )}
                      </div>
                      <p className="font-vt323 text-base text-slate-300 font-mono break-all">
                        {truncateHash(log.transaction_id)}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Checkmark */}
              <div className="w-10 h-10 bg-green-600 border-2 border-green-400 flex items-center justify-center flex-shrink-0">
                <span className="text-white text-2xl">✓</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Info Footer */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mt-6 p-5 bg-blue-900/50 border-4 border-blue-500"
      >
        <div className="flex items-start gap-4">
          <span className="text-3xl">ℹ️</span>
          <div>
            <p className="font-press-start text-sm text-blue-400 mb-3">ABOUT MASUMI NETWORK</p>
            <p className="font-vt323 text-lg text-blue-200 leading-relaxed mb-3">
              MASUMI NETWORK PROVIDES DECENTRALIZED IDENTITY AND DECISION LOGGING FOR AI AGENTS ON CARDANO.
              EACH DECISION IS CRYPTOGRAPHICALLY HASHED AND RECORDED ON-CHAIN.
            </p>
            <a
              href="https://docs.masumi.network"
              target="_blank"
              className="pixel-btn bg-blue-600 border-blue-400 hover:bg-blue-700 inline-flex items-center gap-2"
            >
              LEARN MORE
              <span>→</span>
            </a>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
