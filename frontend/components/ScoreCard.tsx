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
  const getGradeColor = (grade: string) => {
    const colors = {
      'A': 'bg-green-500',
      'B': 'bg-blue-500',
      'C': 'bg-yellow-500',
      'D': 'bg-orange-500',
      'F': 'bg-red-500'
    }
    return colors[grade as keyof typeof colors] || 'bg-gray-500'
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-blue-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  const scores = [
    { label: 'Liquidity', value: score.liquidity_score, weight: '30%' },
    { label: 'Holder Distribution', value: score.holder_distribution_score, weight: '25%' },
    { label: 'Metadata', value: score.metadata_score, weight: '15%' },
    { label: 'Security', value: score.security_score, weight: '15%' },
    { label: 'Supply Stability', value: score.supply_stability_score, weight: '10%' },
    { label: 'Market Activity', value: score.market_activity_score, weight: '5%' },
  ]

  return (
    <div className="bg-gradient-to-r from-cardano-blue to-indigo-600 rounded-xl shadow-lg p-8 mb-6 text-white relative overflow-hidden">
      {/* AI Badge */}
      <div className="absolute top-4 right-4">
        <div className="flex items-center gap-2 bg-white bg-opacity-20 backdrop-blur-sm px-4 py-2 rounded-full border border-white border-opacity-30">
          <span className="text-xl">🤖</span>
          <div className="text-left">
            <div className="text-xs font-bold">AI-POWERED</div>
            <div className="text-xs opacity-75">Gemini Analysis</div>
          </div>
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse ml-1"></span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mt-8">
        {/* Overall Score */}
        <div className="text-center">
          <p className="text-sm opacity-90 mb-2">Listing Readiness Score</p>
          <div className="flex items-center justify-center space-x-4">
            <div className="text-7xl font-bold">{score.total_score}</div>
            <div>
              <div className={`${getGradeColor(score.grade)} px-6 py-2 rounded-lg text-3xl font-bold`}>
                {score.grade}
              </div>
              <p className="text-xs mt-1 opacity-75">Grade</p>
            </div>
          </div>
          <div className="mt-4 bg-white bg-opacity-20 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-white h-full rounded-full transition-all duration-1000"
              style={{ width: `${score.total_score}%` }}
            />
          </div>
        </div>

        {/* Score Breakdown */}
        <div>
          <p className="text-sm opacity-90 mb-4">Score Breakdown</p>
          <div className="space-y-3">
            {scores.map((item, index) => (
              <div key={index}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{item.label} <span className="opacity-75">({item.weight})</span></span>
                  <span className="font-semibold">{item.value.toFixed(1)}/100</span>
                </div>
                <div className="bg-white bg-opacity-20 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-white h-full rounded-full transition-all duration-1000"
                    style={{ width: `${item.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
