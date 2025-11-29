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
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(num)
  }

  const metricCards = [
    {
      label: 'Holder Count',
      value: formatNumber(metrics.holder_count),
      icon: '👥',
      color: 'blue'
    },
    {
      label: 'Total Liquidity',
      value: formatCurrency(metrics.liquidity_usd),
      icon: '💧',
      color: 'green'
    },
    {
      label: '24h Volume',
      value: formatCurrency(metrics.volume_24h),
      icon: '📈',
      color: 'purple'
    },
    {
      label: 'Top 10 Holdings',
      value: `${metrics.top_10_concentration.toFixed(1)}%`,
      icon: '🐋',
      color: 'orange'
    }
  ]

  return (
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-4">Token Metrics</h3>
      
      {/* Metric Cards */}
      <div className="grid md:grid-cols-4 gap-4 mb-6">
        {metricCards.map((metric, index) => (
          <div key={index} className="bg-gradient-to-br from-gray-50 to-white rounded-lg p-4 border border-gray-200">
            <div className="text-2xl mb-2">{metric.icon}</div>
            <div className="text-2xl font-bold text-gray-900">{metric.value}</div>
            <div className="text-sm text-gray-600">{metric.label}</div>
          </div>
        ))}
      </div>

      {/* Detailed Metrics Table */}
      <div className="bg-gray-50 rounded-lg p-4">
        <table className="w-full text-sm">
          <tbody>
            <tr className="border-b border-gray-200">
              <td className="py-2 font-medium text-gray-700">Total Supply</td>
              <td className="py-2 text-right text-gray-900">{formatNumber(parseInt(metrics.total_supply))}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 font-medium text-gray-700">Circulating Supply</td>
              <td className="py-2 text-right text-gray-900">{formatNumber(parseInt(metrics.circulating_supply))}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 font-medium text-gray-700">Top 50 Concentration</td>
              <td className="py-2 text-right text-gray-900">{metrics.top_50_concentration.toFixed(1)}%</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 font-medium text-gray-700">Metadata Quality Score</td>
              <td className="py-2 text-right text-gray-900">{metrics.metadata_score.toFixed(0)}/100</td>
            </tr>
            <tr>
              <td className="py-2 font-medium text-gray-700">Contract Risk Score</td>
              <td className="py-2 text-right text-gray-900">{metrics.contract_risk_score.toFixed(0)}/100</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
