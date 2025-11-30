'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

interface AIInsightsSectionProps {
  readinessScore: any;
  recommendations: any[];
  executiveSummary: string;
  policyId: string;
  targetLiquidity?: number;
  targetChains?: string[];
}

export default function AIInsightsSection({
  readinessScore,
  recommendations,
  executiveSummary,
  policyId,
  targetLiquidity = 0,
  targetChains = ['Ethereum', 'BSC', 'Polygon']
}: AIInsightsSectionProps) {
  const [liquidityPlan, setLiquidityPlan] = useState<any>(null)
  const [bridgeSimulation, setBridgeSimulation] = useState<any>(null)
  
  // Derive a stable key for targetChains to avoid triggering effects
  const chainsKey = Array.isArray(targetChains) ? targetChains.join(',') : String(targetChains)

  useEffect(() => {
    console.log('[AIInsightsSection] Mounted. Props:', { policyId, targetLiquidity, targetChains });
    console.log('[AIInsightsSection] All props received:', { 
      readinessScore, 
      recommendations, 
      executiveSummary, 
      policyId, 
      targetLiquidity, 
      targetChains 
    });
    
    if (policyId) {
      console.log('[AIInsightsSection] Fetching liquidity plan...');
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const liquidityUrl = `${API_BASE}/api/liquidity-plan/${encodeURIComponent(policyId)}?target_liquidity=${encodeURIComponent(targetLiquidity)}`;
      fetch(liquidityUrl)
        .then(res => {
          if (!res.ok) {
            console.error('[AIInsightsSection] Liquidity Plan fetch failed:', res.status, res.statusText, liquidityUrl);
            throw new Error('Liquidity Plan fetch failed');
          }
          return res.json();
        })
        .then(data => {
          setLiquidityPlan(data);
          console.log('Liquidity Plan:', data);
        })
        .catch(err => {
          setLiquidityPlan(null);
          console.error('[AIInsightsSection] Liquidity Plan error:', err, liquidityUrl);
        });

      console.log('[AIInsightsSection] Fetching bridge simulation...');
      const chainsParam = encodeURIComponent((Array.isArray(targetChains) ? targetChains.join(',') : targetChains));
      const bridgeUrl = `${API_BASE}/api/bridge-simulation/${encodeURIComponent(policyId)}?target_chains=${chainsParam}`;
      fetch(bridgeUrl)
        .then(res => {
          if (!res.ok) {
            console.error('[AIInsightsSection] Bridge Simulation fetch failed:', res.status, res.statusText, bridgeUrl);
            throw new Error('Bridge Simulation fetch failed');
          }
          return res.json();
        })
        .then(data => {
          setBridgeSimulation(data);
          console.log('Bridge Simulation:', data);
        })
        .catch(err => {
          setBridgeSimulation(null);
          console.error('[AIInsightsSection] Bridge Simulation error:', err, bridgeUrl);
        });
    } else {
      console.warn('[AIInsightsSection] No policyId provided, skipping API calls');
    }
  }, [policyId, targetLiquidity, chainsKey]);
  
  const [expandedInsight, setExpandedInsight] = useState<string | null>(null)

  // Defensive display values for liquidity plan
  const displayAdaToAdd = (() => {
    if (!liquidityPlan) return 'N/A'
    if (liquidityPlan.ada_to_add !== undefined && liquidityPlan.ada_to_add !== null) return `${liquidityPlan.ada_to_add} ADA`
    if (liquidityPlan.ada_to_add_usd !== undefined && liquidityPlan.ada_to_add_usd !== null) return `${liquidityPlan.ada_to_add_usd} USD (convert to ADA)`
    return 'N/A'
  })()

  const insights = [
    {
      id: 'overview',
      title: 'ANALYSIS OVERVIEW',
      icon: '📊',
      content: executiveSummary || 'No executive summary available',
      highlight: true
    },
    {
      id: 'actionable',
      title: 'ACTIONABLE STRATEGIES',
      icon: '🎯',
      content: (
        <>
          {/* Debug info */}
          <div className="mb-4 p-3 bg-slate-800/60 border border-slate-600 rounded text-xs">
            <p className="text-yellow-300 mb-1">Debug Info:</p>
            <p className="text-slate-300">PolicyId: {policyId || 'Not provided'}</p>
            <p className="text-slate-300">Liquidity Plan: {liquidityPlan ? 'Loaded ✓' : 'Not loaded ✗'}</p>
            <p className="text-slate-300">Bridge Sim: {bridgeSimulation ? 'Loaded ✓' : 'Not loaded ✗'}</p>
          </div>

          {!liquidityPlan && !bridgeSimulation && (
            <div className="p-4 bg-yellow-900/30 border-2 border-yellow-600 rounded">
              <p className="font-vt323 text-lg text-yellow-200">
                {policyId 
                  ? '⏳ Loading actionable strategies...' 
                  : '⚠️ No policy ID provided. Unable to generate strategies.'}
              </p>
            </div>
          )}
          
          {/* Liquidity Plan Details (Live) */}
          {liquidityPlan && (
            <div className="mb-4 p-4 bg-blue-950/40 border-2 border-blue-700 rounded-lg">
              <h4 className="font-press-start text-sm text-blue-300 mb-3 flex items-center gap-2">
                <span>💧</span>
                LIQUIDITY OPTIMIZATION PLAN
              </h4>
              <div className="font-vt323 text-base text-blue-200 space-y-3">
                <div className="grid grid-cols-2 gap-4 mb-3">
                  <div className="bg-blue-900/40 p-3 border border-blue-600 rounded">
                    <p className="text-blue-400 text-sm mb-1">Target Addition</p>
                    <p className="text-xl font-bold">{displayAdaToAdd}</p>
                  </div>
                  <div className="bg-blue-900/40 p-3 border border-blue-600 rounded">
                    <p className="text-blue-400 text-sm mb-1">Optimal Pool</p>
                    <p className="text-lg font-bold">{liquidityPlan.optimal_pool_pair}</p>
                  </div>
                </div>
                
                <div className="bg-blue-900/40 p-3 border border-blue-600 rounded">
                  <p className="text-blue-400 text-sm mb-2">Recommended Split</p>
                  <div className="flex gap-3">
                    {(() => {
                      const split = liquidityPlan?.liquidity_split || { ADA: 0, Other: 0 };
                      const adaPct = Number.isFinite(Number(split.ADA)) ? Math.round(Number(split.ADA) * 100) : 0;
                      const otherPct = Number.isFinite(Number(split.Other)) ? Math.round(Number(split.Other) * 100) : 0;
                      return (
                        <>
                          <span className="px-3 py-1 bg-blue-800 rounded">ADA: {adaPct}%</span>
                          <span className="px-3 py-1 bg-blue-800 rounded">Other: {otherPct}%</span>
                        </>
                      )
                    })()}
                  </div>
                </div>

                <div className="bg-blue-900/40 p-3 border border-blue-600 rounded">
                  <p className="text-blue-400 text-sm mb-2">Sample Transaction</p>
                  <pre className="bg-slate-900/60 p-3 rounded text-xs overflow-x-auto">
                    {JSON.stringify(liquidityPlan.sample_transaction, null, 2)}
                  </pre>
                </div>

                <div className="bg-blue-900/40 p-3 border border-blue-600 rounded">
                  <p className="text-blue-400 text-sm mb-2">📅 Liquidity Deployment Schedule</p>
                  <div className="space-y-2">
                    {((liquidityPlan?.liquidity_schedule) || []).map((item: any, idx: number) => (
                      <div key={idx} className="flex justify-between items-center bg-blue-950/40 p-2 rounded">
                        <span className="text-blue-300">Week {item.week}</span>
                        <span className="text-blue-100">{item.date}</span>
                        <span className="text-blue-300 font-bold">{item.ada_amount ?? item.ada ?? 'N/A'} ADA</span>
                      </div>
                    ))}
                    {(!(liquidityPlan?.liquidity_schedule) || (liquidityPlan?.liquidity_schedule || []).length === 0) && (
                      <div className="text-sm text-blue-300">No schedule available</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Bridge Simulation Details (Live) */}
          {bridgeSimulation && (
            <div className="p-4 bg-purple-950/40 border-2 border-purple-700 rounded-lg">
              <h4 className="font-press-start text-sm text-purple-300 mb-3 flex items-center gap-2">
                <span>🌉</span>
                CROSS-CHAIN BRIDGE ANALYSIS
              </h4>
              <div className="font-vt323 text-base text-purple-200 space-y-3">
                <div className="bg-purple-900/40 p-3 border border-purple-600 rounded">
                  <p className="text-purple-400 text-sm mb-2">🎯 Recommended Chain</p>
                  <p className="text-2xl font-bold text-purple-100 mb-2">
                    {bridgeSimulation.recommended_chain}
                  </p>
                  <p className="text-base text-purple-200">
                    {bridgeSimulation.recommendation_reasoning}
                  </p>
                </div>

                <div className="bg-purple-900/40 p-3 border border-purple-600 rounded">
                  <p className="text-purple-400 text-sm mb-3">Available Bridge Routes</p>
                  <div className="space-y-2">
                    {bridgeSimulation.routes.map((route: any, idx: number) => (
                      <div key={idx} className="bg-purple-950/60 p-3 border border-purple-700 rounded">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xl">🔗</span>
                          <span className="font-bold text-purple-100">
                            {route.source_chain} → {route.target_chain}
                          </span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                          <div>
                            <span className="text-purple-400">Bridge: </span>
                            <span className="text-purple-200">{route.bridge_name}</span>
                          </div>
                          <div>
                            <span className="text-purple-400">Fee: </span>
                            <span className="text-purple-200">{route.estimated_fee}</span>
                          </div>
                          <div>
                            <span className="text-purple-400">Time: </span>
                            <span className="text-purple-200">{route.estimated_time}</span>
                          </div>
                          <div>
                            <span className="text-purple-400">Trust: </span>
                            <span className="text-purple-200">{route.trust_model}</span>
                          </div>
                        </div>
                        <div className="mt-2 pt-2 border-t border-purple-700">
                          <span className="text-purple-400">Score: </span>
                          <span className="text-purple-100 font-bold">{route.recommendation_score}/100</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      ),
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
      {/* AI Badge removed per request */}

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
                <div className="font-vt323 text-xl text-slate-200 leading-relaxed whitespace-pre-line">
                  {insight.content}
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  )
}