import { motion } from 'framer-motion'

interface ScoreCardProps {
  score: {
    total_score: number
    grade: string
    liquidity_score: number
    holder_distribution_score: number
    metadata_score: number
    security_score: number
    supply_stability_score: number
    market_activity_score: number
  }
}

export default function ScoreCard({ score }: ScoreCardProps) {
  const getGradeStyles = (grade: string) => {
    const styles: Record<string, { bg: string; border: string; text: string }> = {
      'A': { bg: 'bg-green-600', border: 'border-green-400', text: 'text-white' },
      'B': { bg: 'bg-blue-600', border: 'border-blue-400', text: 'text-white' },
      'C': { bg: 'bg-yellow-600', border: 'border-yellow-400', text: 'text-white' },
      'D': { bg: 'bg-orange-600', border: 'border-orange-400', text: 'text-white' },
      'F': { bg: 'bg-red-600', border: 'border-red-400', text: 'text-white' }
    }
    return styles[grade] || { bg: 'bg-slate-600', border: 'border-slate-400', text: 'text-white' }
  }

  const getScoreBarColor = (value: number) => {
    if (value >= 75) return 'bg-green-500'
    if (value >= 50) return 'bg-blue-500'
    if (value >= 25) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const scores = [
    { label: 'LIQUIDITY', value: score.liquidity_score, weight: '30%', icon: '💧' },
    { label: 'HOLDER DISTRIBUTION', value: score.holder_distribution_score, weight: '25%', icon: '👥' },
    { label: 'METADATA QUALITY', value: score.metadata_score, weight: '15%', icon: '📝' },
    { label: 'SECURITY', value: score.security_score, weight: '15%', icon: '🔒' },
    { label: 'SUPPLY STABILITY', value: score.supply_stability_score, weight: '10%', icon: '📊' },
    { label: 'MARKET ACTIVITY', value: score.market_activity_score, weight: '5%', icon: '📈' },
  ]

  const gradeStyle = getGradeStyles(score.grade)

  return (
    <div className="pixel-card p-8">
      <div className="grid lg:grid-cols-[320px_1fr] gap-8">
        {/* Overall Score */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col items-center justify-center p-8 bg-slate-900/50 border-4 border-slate-700"
        >
          <p className="font-press-start text-xs text-slate-400 mb-6 tracking-wider">READINESS SCORE</p>

          {/* Score Display */}
          <div className="relative mb-6">
            <div className="w-40 h-40 border-8 border-slate-700 bg-black flex items-center justify-center relative overflow-hidden">
              {/* Animated background */}
              <motion.div
                animate={{
                  backgroundPosition: ['0% 0%', '100% 100%'],
                }}
                transition={{ duration: 3, repeat: Infinity, repeatType: 'reverse' }}
                className="absolute inset-0 opacity-20"
                style={{
                  background: 'linear-gradient(45deg, #3b82f6 0%, #8b5cf6 50%, #3b82f6 100%)',
                  backgroundSize: '200% 200%',
                }}
              />

              <div className="relative z-10 text-center">
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                  className="text-6xl font-press-start text-white block"
                >
                  {score.total_score}
                </motion.span>
                <span className="text-sm font-vt323 text-slate-400 block mt-2">OUT OF 100</span>
              </div>
            </div>
          </div>

          {/* Grade Badge */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className={`${gradeStyle.bg} ${gradeStyle.border} border-4 px-8 py-3 shadow-[4px_4px_0px_0px_#000]`}
          >
            <span className="font-press-start text-2xl text-white">GRADE {score.grade}</span>
          </motion.div>
        </motion.div>

        {/* Score Breakdown */}
        <div>
          <div className="flex items-center justify-between mb-6 pb-4 border-b-4 border-slate-700">
            <h3 className="font-press-start text-sm text-white">SCORE BREAKDOWN</h3>
            <span className="font-press-start text-xs text-slate-500">WEIGHT</span>
          </div>

          <div className="space-y-6">
            {scores.map((item, index) => (
              <motion.div
                key={index}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1 * index }}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{item.icon}</span>
                    <span className="font-press-start text-xs text-slate-300">{item.label}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="font-vt323 text-2xl text-white min-w-[3rem] text-right">{item.value.toFixed(0)}</span>
                    <span className="font-vt323 text-lg text-slate-500 min-w-[3rem] text-right">{item.weight}</span>
                  </div>
                </div>

                {/* Pixel Progress Bar */}
                <div className="h-6 bg-black border-2 border-slate-700 relative overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value}%` }}
                    transition={{ delay: 0.2 * index, duration: 0.8, ease: 'easeOut' }}
                    className={`h-full ${getScoreBarColor(item.value)} relative`}
                  >
                    {/* Pixel pattern overlay */}
                    <div
                      className="absolute inset-0 opacity-30"
                      style={{
                        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.1) 2px, rgba(255,255,255,0.1) 4px)',
                      }}
                    />
                  </motion.div>

                  {/* Score value overlay */}
                  <div className="absolute inset-0 flex items-center justify-end pr-2">
                    <span className="font-press-start text-[10px] text-white drop-shadow-[2px_2px_0px_rgba(0,0,0,0.8)]">
                      {item.value.toFixed(0)}%
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
