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
  const getPriorityBadge = (priority: string) => {
    const styles = {
      high: 'bg-red-100 text-red-800 border-red-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      low: 'bg-green-100 text-green-800 border-green-200'
    }
    return styles[priority as keyof typeof styles] || styles.medium
  }

  const getPriorityIcon = (priority: string) => {
    const icons = {
      high: '🔴',
      medium: '🟡',
      low: '🟢'
    }
    return icons[priority as keyof typeof icons] || '⚪'
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-center">
          <span className="text-3xl mr-3">✅</span>
          <div>
            <h3 className="text-lg font-semibold text-green-900">Excellent!</h3>
            <p className="text-green-700">No critical issues found. Your token is in great shape for CEX listing.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-900">Improvement Recommendations</h3>
        <div className="flex items-center gap-2 px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
          <span>🤖</span>
          AI-Generated
        </div>
      </div>
      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">{getPriorityIcon(rec.priority)}</span>
                <h4 className="text-lg font-semibold text-gray-900">{rec.category}</h4>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getPriorityBadge(rec.priority)}`}>
                  {rec.priority.toUpperCase()} PRIORITY
                </span>
              </div>
            </div>
            
            <div className="space-y-2">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-1">Issue:</p>
                <p className="text-sm text-gray-600">{rec.issue}</p>
              </div>
              
              <div>
                <p className="text-sm font-medium text-gray-700 mb-1">Recommendation:</p>
                <p className="text-sm text-gray-600">{rec.recommendation}</p>
              </div>
              
              <div className="pt-2 border-t border-gray-100">
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Estimated Impact:</span> {rec.estimated_impact}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
