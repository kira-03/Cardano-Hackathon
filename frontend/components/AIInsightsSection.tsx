'use client'

import { useState } from 'react'
// Removed AISymbol import
import { motion } from 'framer-motion'

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

  const insights = [
    {
      id: 'overview',
      title: 'ANALYSIS OVERVIEW',
      icon: '📊',
      content: executiveSummary,
      highlight: true
    },
    {
      id: 'liquidity',
      title: 'LIQUIDITY ASSESSMENT',
      icon: '💧',
      content: readinessScore?.ai_analysis?.liquidity_assessment ||
        `Liquidity score: ${readinessScore?.liquidity_score}/100. ${readinessScore?.liquidity_score >= 70
          ? 'Strong liquidity depth supporting market stability and exchange requirements.'
          : readinessScore?.liquidity_score >= 50
            ? 'Moderate liquidity requiring enhancement for top-tier exchange listings.'
            : 'Limited liquidity depth - priority improvement area for exchange readiness.'
        }`
    },
    {
      id: 'decentralization',
      title: 'HOLDER DISTRIBUTION',
      icon: '👥',
      content: readinessScore?.ai_analysis?.decentralization_review ||
        `Distribution score: ${readinessScore?.holder_distribution_score}/100. ${readinessScore?.holder_distribution_score >= 70
          ? 'Well-distributed token ownership with minimal whale concentration risk.'
          : readinessScore?.holder_distribution_score >= 50
            ? 'Moderate token concentration - consider distribution improvement strategies.'
            : 'High whale concentration detected - implement distribution enhancement programs.'
        }`
    },
    {
      id: 'metadata',
      title: 'METADATA QUALITY',
      icon: '📝',
      content: readinessScore?.ai_analysis?.metadata_evaluation ||
        `Metadata score: ${readinessScore?.metadata_score}/100. ${readinessScore?.metadata_score >= 80
          ? 'Complete and professional token metadata meets exchange standards.'
          : readinessScore?.metadata_score >= 60
            ? 'Metadata partially complete - add missing fields for optimal presentation.'
            : 'Metadata requires significant enhancement with branding and informational content.'
        }`
    },
    {
      id: 'security',
      title: 'SECURITY PROFILE',
      icon: '🔒',
      content: readinessScore?.ai_analysis?.security_analysis ||
        `Security score: ${readinessScore?.security_score}/100. ${readinessScore?.security_score >= 80
          ? 'Strong security profile with low risk factors identified.'
          : readinessScore?.security_score >= 60
            ? 'Acceptable security with room for audit and verification improvements.'
            : 'Security concerns detected - consider professional audit services.'
        }`
    },
    {
      id: 'market',
      title: 'MARKET DYNAMICS',
      icon: '📈',
      content: readinessScore?.ai_analysis?.market_dynamics ||
        `Market activity score: ${readinessScore?.market_activity_score}/100. ${readinessScore?.market_activity_score >= 70
          ? 'Healthy trading patterns with strong volume-to-liquidity ratios.'
          : readinessScore?.market_activity_score >= 40
            ? 'Moderate market activity - enhance through partnerships and market making.'
            : 'Low trading activity - implement strategies to boost market engagement.'
        }`
    }
  ]

  const criticalInsights = readinessScore?.critical_insights || []
  const exchangeReadiness = readinessScore?.exchange_readiness_factors || {}

  return (
    <div className="space-y-6">
      {/* AI Badge Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 border-4 border-purple-500 p-6"
      >
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-purple-600 border-4 border-purple-400 flex items-center justify-center">
            <span className="text-4xl">👾</span>
          </div>
          <div>
            <h2 className="font-press-start text-lg text-white mb-2">INTELLIGENT ANALYSIS</h2>
            <p className="font-vt323 text-xl text-purple-300">POWERED BY OPENAI</p>
          </div>
        </div>

        {/* AI Capabilities */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: 'SCORING', icon: '📊' },
            { label: 'INSIGHTS', icon: '💡' },
            { label: 'RISK ANALYSIS', icon: '⚠️' },
            { label: 'FORECASTING', icon: '🔮' }
          ].map((capability) => (
            <div key={capability.label} className="bg-purple-800/50 border-2 border-purple-600 py-3 px-2 text-center">
              <div className="text-2xl mb-1">{capability.icon}</div>
              <div className="font-press-start text-[10px] text-purple-200">{capability.label}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Critical AI Insights */}
      {criticalInsights.length > 0 && (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-yellow-900/50 border-4 border-yellow-500 p-6"
        >
          <h3 className="font-press-start text-sm text-yellow-400 mb-4 flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            KEY FINDINGS
          </h3>
          <ul className="space-y-3">
            {criticalInsights.map((insight: string, index: number) => (
              <li key={index} className="flex items-start gap-3 font-vt323 text-lg text-yellow-200">
                <span className="text-yellow-400 text-2xl">▸</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* Exchange Readiness Factors */}
      {(exchangeReadiness.immediate_strengths?.length > 0 ||
        exchangeReadiness.improvement_needed?.length > 0 ||
        exchangeReadiness.risk_factors?.length > 0) && (
          <div className="grid sm:grid-cols-3 gap-4">
            {exchangeReadiness.immediate_strengths?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-green-900/50 border-4 border-green-500 p-5"
              >
                <h4 className="font-press-start text-xs text-green-400 mb-4 flex items-center gap-2">
                  <span className="text-xl">✓</span>
                  STRENGTHS
                </h4>
                <ul className="space-y-2">
                  {exchangeReadiness.immediate_strengths.map((strength: string, index: number) => (
                    <li key={index} className="font-vt323 text-base text-green-200 flex items-start gap-2">
                      <span className="text-green-400">•</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}

            {exchangeReadiness.improvement_needed?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-blue-900/50 border-4 border-blue-500 p-5"
              >
                <h4 className="font-press-start text-xs text-blue-400 mb-4 flex items-center gap-2">
                  <span className="text-xl">⚡</span>
                  IMPROVEMENTS
                </h4>
                <ul className="space-y-2">
                  {exchangeReadiness.improvement_needed.map((improvement: string, index: number) => (
                    <li key={index} className="font-vt323 text-base text-blue-200 flex items-start gap-2">
                      <span className="text-blue-400">•</span>
                      {improvement}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}

            {exchangeReadiness.risk_factors?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-red-900/50 border-4 border-red-500 p-5"
              >
                <h4 className="font-press-start text-xs text-red-400 mb-4 flex items-center gap-2">
                  <span className="text-xl">⚠</span>
                  RISK FACTORS
                </h4>
                <ul className="space-y-2">
                  {exchangeReadiness.risk_factors.map((risk: string, index: number) => (
                    <li key={index} className="font-vt323 text-base text-red-200 flex items-start gap-2">
                      <span className="text-red-400">•</span>
                      {risk}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}
          </div>
        )}

      {/* Detailed AI Insights */}
      <div className="space-y-3">
        {insights.map((insight, index) => (
          <motion.div
            key={insight.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`bg-slate-900/50 border-4 ${insight.highlight
                ? 'border-blue-500'
                : 'border-slate-700'
              } overflow-hidden`}
          >
            <button
              onClick={() => setExpandedInsight(
                expandedInsight === insight.id ? null : insight.id
              )}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/50 transition-colors border-b-4 border-slate-700"
            >
              <div className="flex items-center gap-4">
                <span className="text-3xl">{insight.icon}</span>
                <span className="font-press-start text-xs text-white">{insight.title}</span>
              </div>
              <span className={`text-2xl transition-transform ${expandedInsight === insight.id ? 'rotate-180' : ''
                }`}>
                ▼
              </span>
            </button>

            {expandedInsight === insight.id && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="px-6 py-5 bg-slate-800/30"
              >
                <p className="font-vt323 text-xl text-slate-200 leading-relaxed whitespace-pre-line">
                  {insight.content}
                </p>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  )
}
