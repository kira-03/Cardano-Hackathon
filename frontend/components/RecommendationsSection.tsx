import { motion } from 'framer-motion'

interface Recommendation {
  category: string
  priority: string
  issue: string
  recommendation: string
  estimated_impact: string
}

interface RecommendationsSectionProps {
  recommendations: Recommendation[]
}

export default function RecommendationsSection({ recommendations }: RecommendationsSectionProps) {
  const getPriorityStyles = (priority: string) => {
    const styles: Record<string, { bg: string; border: string; icon: string }> = {
      high: { bg: 'bg-red-600', border: 'border-red-400', icon: '🚨' },
      medium: { bg: 'bg-yellow-600', border: 'border-yellow-400', icon: '⚠️' },
      low: { bg: 'bg-green-600', border: 'border-green-400', icon: '✅' }
    }
    return styles[priority.toLowerCase()] || styles.medium
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-green-900/50 border-4 border-green-500 p-6 flex items-center gap-4"
      >
        <div className="w-16 h-16 bg-green-600 border-4 border-green-400 flex items-center justify-center">
          <span className="text-4xl">✓</span>
        </div>
        <div>
          <h3 className="font-press-start text-sm text-green-400 mb-2">LOOKING GOOD!</h3>
          <p className="font-vt323 text-xl text-green-300">NO CRITICAL ISSUES FOUND. TOKEN READY FOR CEX LISTING.</p>
        </div>
      </motion.div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-press-start text-lg text-white flex items-center gap-3">
          <span className="text-2xl">💡</span>
          RECOMMENDATIONS
        </h3>
        <span className="pixel-tag bg-blue-600 border-blue-400 text-white">
          {recommendations.length} ITEMS
        </span>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec, index) => {
          const styles = getPriorityStyles(rec.priority)
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-slate-900/50 border-4 border-slate-700 hover:border-slate-600 transition-colors"
            >
              {/* Header */}
              <div className="flex items-center justify-between gap-4 p-5 border-b-4 border-slate-700 bg-slate-800/50">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{styles.icon}</span>
                  <h4 className="font-press-start text-sm text-white uppercase">{rec.category}</h4>
                </div>
                <span className={`${styles.bg} ${styles.border} border-2 px-3 py-1 font-press-start text-xs text-white uppercase`}>
                  {rec.priority}
                </span>
              </div>

              {/* Content */}
              <div className="p-5 space-y-4">
                <div>
                  <p className="font-press-start text-[10px] text-slate-500 uppercase tracking-wide mb-2">⚠️ ISSUE</p>
                  <p className="font-vt323 text-lg text-slate-300 leading-relaxed">{rec.issue}</p>
                </div>

                <div>
                  <p className="font-press-start text-[10px] text-slate-500 uppercase tracking-wide mb-2">💡 RECOMMENDATION</p>
                  <p className="font-vt323 text-lg text-white leading-relaxed">{rec.recommendation}</p>
                </div>

                <div className="pt-4 border-t-2 border-slate-700">
                  <p className="font-vt323 text-base text-slate-400">
                    <span className="font-press-start text-xs text-slate-500">EXPECTED IMPACT:</span> {rec.estimated_impact}
                  </p>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
