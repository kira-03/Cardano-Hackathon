'use client'

import { useState } from 'react'

interface AIInsightsSectionProps {
  readinessScore: any
  recommendations: any[]
  executiveSummary: string
}

export default function AIInsightsSection({ 
  readinessScore, 
  recommendations,
  executiveSummary 
}: AIInsightsSectionProps) {
  const [expandedInsight, setExpandedInsight] = useState<string | null>('overview')

  // Check if AI-generated insights are available
  const hasAIAnalysis = readinessScore?.ai_analysis || false
  const hasAIRecommendations = recommendations?.some((rec: any) => 
    rec.implementation_timeline || rec.success_metrics
  )

  const insights = [
    {
      id: 'overview',
      title: '🤖 AI Analysis Overview',
      icon: '🧠',
      badge: 'Gemini AI',
      content: executiveSummary,
      highlight: true
    },
    {
      id: 'liquidity',
      title: 'Liquidity Assessment',
      icon: '💰',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.liquidity_assessment || 
        `Current liquidity score: ${readinessScore?.liquidity_score}/100. ${
          readinessScore?.liquidity_score >= 70 
            ? 'Strong liquidity depth supporting market stability and exchange requirements.' 
            : readinessScore?.liquidity_score >= 50
            ? 'Moderate liquidity requiring enhancement for top-tier exchange listings.'
            : 'Limited liquidity depth - priority improvement area for exchange readiness.'
        }`
    },
    {
      id: 'decentralization',
      title: 'Decentralization Review',
      icon: '👥',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.decentralization_review ||
        `Holder distribution score: ${readinessScore?.holder_distribution_score}/100. ${
          readinessScore?.holder_distribution_score >= 70
            ? 'Well-distributed token ownership with minimal whale concentration risk.'
            : readinessScore?.holder_distribution_score >= 50
            ? 'Moderate token concentration - consider distribution improvement strategies.'
            : 'High whale concentration detected - implement distribution enhancement programs.'
        }`
    },
    {
      id: 'metadata',
      title: 'Metadata Evaluation',
      icon: '📝',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.metadata_evaluation ||
        `Metadata quality score: ${readinessScore?.metadata_score}/100. ${
          readinessScore?.metadata_score >= 80
            ? 'Complete and professional token metadata meets exchange standards.'
            : readinessScore?.metadata_score >= 60
            ? 'Metadata partially complete - add missing fields for optimal presentation.'
            : 'Metadata requires significant enhancement with branding and informational content.'
        }`
    },
    {
      id: 'security',
      title: 'Security Analysis',
      icon: '🔒',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.security_analysis ||
        `Security score: ${readinessScore?.security_score}/100. ${
          readinessScore?.security_score >= 80
            ? 'Strong security profile with low risk factors identified.'
            : readinessScore?.security_score >= 60
            ? 'Acceptable security with room for audit and verification improvements.'
            : 'Security concerns detected - consider professional audit services.'
        }`
    },
    {
      id: 'market',
      title: 'Market Dynamics',
      icon: '📊',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.market_dynamics ||
        `Market activity score: ${readinessScore?.market_activity_score}/100. ${
          readinessScore?.market_activity_score >= 70
            ? 'Healthy trading patterns with strong volume-to-liquidity ratios.'
            : readinessScore?.market_activity_score >= 40
            ? 'Moderate market activity - enhance through partnerships and market making.'
            : 'Low trading activity - implement strategies to boost market engagement.'
        }`
    },
    {
      id: 'growth',
      title: 'Growth Outlook',
      icon: '📈',
      badge: 'AI Powered',
      content: readinessScore?.ai_analysis?.growth_outlook ||
        `Overall grade: ${readinessScore?.grade}. ${
          readinessScore?.grade === 'A'
            ? 'Exceptional fundamentals with strong exchange listing potential and growth trajectory.'
            : readinessScore?.grade === 'B'
            ? 'Solid foundation with good growth prospects - minor optimizations recommended.'
            : readinessScore?.grade === 'C'
            ? 'Developing potential requiring strategic improvements in key areas.'
            : readinessScore?.grade === 'D'
            ? 'Early-stage token needing significant enhancement before exchange consideration.'
            : 'Requires comprehensive improvement across multiple dimensions for market viability.'
        }`
    }
  ]

  // Extract AI-specific insights
  const criticalInsights = readinessScore?.critical_insights || []
  const exchangeReadiness = readinessScore?.exchange_readiness_factors || {}

  return (
    <div className="space-y-6">
      {/* AI Badge Header */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl">🤖</span>
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">AI-Powered Analysis</h2>
            <p className="text-sm text-slate-600">Generated by Google Gemini 2.5 Flash</p>
          </div>
          <div className="ml-auto">
            <span className="px-3 py-1 bg-green-500 text-white text-xs font-bold rounded-full flex items-center gap-1">
              <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
              AI ACTIVE
            </span>
          </div>
        </div>
        
        {/* AI Capabilities */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
            <div className="text-2xl mb-1">🧠</div>
            <div className="text-xs font-semibold text-slate-700">Smart Scoring</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
            <div className="text-2xl mb-1">💡</div>
            <div className="text-xs font-semibold text-slate-700">Recommendations</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
            <div className="text-2xl mb-1">🎯</div>
            <div className="text-xs font-semibold text-slate-700">Risk Analysis</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
            <div className="text-2xl mb-1">📈</div>
            <div className="text-xs font-semibold text-slate-700">Growth Insights</div>
          </div>
        </div>
      </div>

      {/* Critical AI Insights */}
      {criticalInsights.length > 0 && (
        <div className="bg-amber-50 border-l-4 border-amber-500 rounded-lg p-5">
          <h3 className="font-bold text-slate-900 mb-3 flex items-center gap-2">
            <span>⚡</span>
            Critical AI Insights
          </h3>
          <ul className="space-y-2">
            {criticalInsights.map((insight: string, index: number) => (
              <li key={index} className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-amber-600 font-bold">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Exchange Readiness Factors */}
      {(exchangeReadiness.immediate_strengths?.length > 0 || 
        exchangeReadiness.improvement_needed?.length > 0 ||
        exchangeReadiness.risk_factors?.length > 0) && (
        <div className="grid md:grid-cols-3 gap-4">
          {/* Strengths */}
          {exchangeReadiness.immediate_strengths?.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-900 mb-2 flex items-center gap-2">
                <span>✅</span>
                Immediate Strengths
              </h4>
              <ul className="space-y-1">
                {exchangeReadiness.immediate_strengths.map((strength: string, index: number) => (
                  <li key={index} className="text-sm text-green-800">• {strength}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Improvements Needed */}
          {exchangeReadiness.improvement_needed?.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                <span>🔧</span>
                Improvement Needed
              </h4>
              <ul className="space-y-1">
                {exchangeReadiness.improvement_needed.map((improvement: string, index: number) => (
                  <li key={index} className="text-sm text-blue-800">• {improvement}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk Factors */}
          {exchangeReadiness.risk_factors?.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
                <span>⚠️</span>
                Risk Factors
              </h4>
              <ul className="space-y-1">
                {exchangeReadiness.risk_factors.map((risk: string, index: number) => (
                  <li key={index} className="text-sm text-red-800">• {risk}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Detailed AI Insights */}
      <div className="space-y-3">
        {insights.map((insight) => (
          <div 
            key={insight.id}
            className={`border rounded-lg overflow-hidden transition-all ${
              insight.highlight 
                ? 'border-purple-300 bg-gradient-to-r from-purple-50 to-blue-50' 
                : 'border-slate-200 bg-white'
            }`}
          >
            <button
              onClick={() => setExpandedInsight(
                expandedInsight === insight.id ? null : insight.id
              )}
              className="w-full px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{insight.icon}</span>
                <div className="text-left">
                  <h3 className="font-semibold text-slate-900">{insight.title}</h3>
                  {insight.badge && (
                    <span className="text-xs text-purple-600 font-medium">{insight.badge}</span>
                  )}
                </div>
              </div>
              <svg 
                className={`w-5 h-5 text-slate-400 transition-transform ${
                  expandedInsight === insight.id ? 'rotate-180' : ''
                }`}
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {expandedInsight === insight.id && (
              <div className="px-5 pb-4 pt-2 border-t border-slate-200">
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
                  {insight.content}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* AI Recommendations with Timeline */}
      {hasAIRecommendations && (
        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <h3 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
            <span>🎯</span>
            AI Strategic Recommendations
          </h3>
          <div className="space-y-4">
            {recommendations
              .filter((rec: any) => rec.implementation_timeline || rec.success_metrics)
              .map((rec: any, index: number) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <span className={`text-xs font-bold px-2 py-1 rounded ${
                        rec.priority === 'high' 
                          ? 'bg-red-100 text-red-700' 
                          : rec.priority === 'medium'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {rec.priority?.toUpperCase()}
                      </span>
                      <span className="ml-2 text-xs text-slate-500">{rec.category}</span>
                    </div>
                  </div>
                  <p className="text-sm font-semibold text-slate-900 mb-1">{rec.recommendation}</p>
                  
                  {rec.implementation_timeline && (
                    <p className="text-xs text-slate-600 mt-2">
                      <span className="font-semibold">⏱️ Timeline:</span> {rec.implementation_timeline}
                    </p>
                  )}
                  
                  {rec.success_metrics && (
                    <p className="text-xs text-slate-600 mt-1">
                      <span className="font-semibold">📊 Success Metrics:</span> {rec.success_metrics}
                    </p>
                  )}
                  
                  <p className="text-xs text-blue-600 mt-2">
                    <span className="font-semibold">💫 Impact:</span> {rec.estimated_impact}
                  </p>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* AI Footer Note */}
      <div className="text-center text-xs text-slate-500 italic">
        💡 Analysis generated by Google Gemini AI • Real-time insights based on blockchain data
      </div>
    </div>
  )
}
