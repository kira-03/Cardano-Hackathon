import { motion } from 'framer-motion'

interface MetricsSectionProps {
  metrics: {
    total_supply: string
    circulating_supply: string
    holder_count: number
    top_10_concentration: number
    top_50_concentration: number
    liquidity_usd: number
    volume_24h: number
    metadata_score: number
    contract_risk_score: number
  }
}

export default function MetricsSection({ metrics }: MetricsSectionProps) {
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: 0
    }).format(num)
  }

  const formatCurrency = (num: number) => {
    if (num >= 1000000) {
      return `$${(num / 1000000).toFixed(2)}M`
    }
    if (num >= 1000) {
      return `$${(num / 1000).toFixed(1)}K`
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(num)
  }

  const metricCards = [
    {
      label: 'HOLDER COUNT',
      value: formatNumber(metrics.holder_count),
      subtext: 'UNIQUE ADDRESSES',
      icon: '👥',
      color: 'blue'
    },
    {
      label: 'TOTAL LIQUIDITY',
      value: formatCurrency(metrics.liquidity_usd),
      subtext: 'ACROSS POOLS',
      icon: '💧',
      color: 'green'
    },
    {
      label: '24H VOLUME',
      value: formatCurrency(metrics.volume_24h),
      subtext: 'TRADING VOLUME',
      icon: '📈',
      color: 'purple'
    },
    {
      label: 'TOP 10 HOLDINGS',
      value: `${metrics.top_10_concentration.toFixed(1)}%`,
      subtext: 'CONCENTRATION',
      icon: '🎯',
      color: 'yellow'
    }
  ]

  const detailedMetrics = [
    { label: 'TOTAL SUPPLY', value: formatNumber(parseInt(metrics.total_supply)), icon: '📦' },
    { label: 'CIRCULATING SUPPLY', value: formatNumber(parseInt(metrics.circulating_supply)), icon: '🔄' },
    { label: 'TOP 50 CONCENTRATION', value: `${metrics.top_50_concentration.toFixed(1)}%`, icon: '📊' },
    { label: 'METADATA QUALITY', value: `${metrics.metadata_score.toFixed(0)} / 100`, icon: '📝' },
    { label: 'CONTRACT RISK SCORE', value: `${metrics.contract_risk_score.toFixed(0)} / 100`, icon: '🔒' },
  ]

  return (
    <div>
      <h3 className="font-press-start text-lg text-white mb-6 flex items-center gap-3">
        <span className="text-2xl">📊</span>
        TOKEN METRICS
      </h3>

      {/* Metric Cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {metricCards.map((metric, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-900/50 border-4 border-slate-700 p-5 hover:border-slate-600 transition-colors"
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="text-3xl">{metric.icon}</span>
              <p className="font-press-start text-[10px] text-slate-400 uppercase tracking-wide">{metric.label}</p>
            </div>
            <p className="font-vt323 text-4xl text-white mb-1">{metric.value}</p>
            <p className="font-vt323 text-sm text-slate-500 uppercase">{metric.subtext}</p>
          </motion.div>
        ))}
      </div>

      {/* Detailed Metrics */}
      <div className="bg-slate-900/50 border-4 border-slate-700">
        <div className="border-b-4 border-slate-700 bg-slate-800/50 px-6 py-4">
          <h4 className="font-press-start text-xs text-white">DETAILED METRICS</h4>
        </div>
        <div className="divide-y-2 divide-slate-700">
          {detailedMetrics.map((metric, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + index * 0.1 }}
              className="px-6 py-4 hover:bg-slate-800/30 transition-colors flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{metric.icon}</span>
                <span className="font-press-start text-xs text-slate-300">{metric.label}</span>
              </div>
              <span className="font-vt323 text-2xl text-white">{metric.value}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
