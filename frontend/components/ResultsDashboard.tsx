'use client'

import { useState } from 'react'
import ScoreCard from './ScoreCard'
import MetricsSection from './MetricsSection'
import RecommendationsSection from './RecommendationsSection'
import ExchangeRequirementsSection from './ExchangeRequirementsSection'
import BridgeRoutesSection from './BridgeRoutesSection'
import MasumiLogsSection from './MasumiLogsSection'
import AIInsightsSection from './AIInsightsSection'

interface ResultsDashboardProps {
  result: any
  onNewAnalysis: () => void
}

export default function ResultsDashboard({ result, onNewAnalysis }: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview')

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'ai-insights', label: '🤖 AI Insights', icon: '🧠' },
    { id: 'exchange', label: 'Exchange Prep', icon: '📋' },
    { id: 'bridges', label: 'Bridge Routes', icon: '🌉' },
    { id: 'masumi', label: 'Audit Log', icon: '🔒' },
  ]

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {result.token_name} ({result.token_symbol})
            </h1>
            <p className="text-sm text-slate-600 mt-1 font-mono">
              {result.policy_id.slice(0, 30)}...{result.policy_id.slice(-10)}
            </p>
            <p className="text-xs text-slate-400 mt-1">
              ID: {result.analysis_id.slice(0, 8)}
            </p>
          </div>
          <div className="flex gap-3">
            <a
              href={`http://localhost:8000/api/analysis/${result.analysis_id}/pdf`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-5 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors shadow-sm flex items-center gap-2 font-medium"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF
            </a>
            <button
              onClick={onNewAnalysis}
              className="px-5 py-2.5 bg-slate-100 text-slate-700 rounded-md hover:bg-slate-200 transition-colors font-medium"
            >
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Score Card */}
      <ScoreCard score={result.readiness_score} />

      {/* Executive Summary */}
      <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 border-2 border-purple-200 rounded-lg p-6 mb-6 relative overflow-hidden">
        {/* AI Sparkle Effect */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-300 to-blue-300 rounded-full blur-3xl opacity-20"></div>
        
        <div className="relative">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-900 flex items-center gap-2">
              <span className="text-2xl">📊</span>
              Executive Summary
            </h2>
            <div className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full text-xs font-bold shadow-md">
              <span>🤖</span>
              AI-Generated Insights
              <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
            </div>
          </div>
          <div 
            className="text-sm leading-relaxed text-slate-700 bg-white bg-opacity-60 rounded-lg p-4 border border-purple-100"
            dangerouslySetInnerHTML={{ __html: result.executive_summary.replace(/\n/g, '<br />') }}
          />
        </div>
      </div>

      {/* Next Steps */}
      <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">Next Steps</h2>
        <ul className="space-y-3">
          {result.next_steps.map((step: string, index: number) => (
            <li key={index} className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">{index + 1}</span>
              <span className="text-slate-700">{step}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Tabs */}
      <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
        {/* Tab Headers */}
        <div className="border-b border-slate-200 bg-slate-50">
          <div className="flex">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-6 py-3 text-center font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-white text-blue-600 border-b-2 border-blue-600 -mb-px'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <MetricsSection metrics={result.metrics} />
              <RecommendationsSection recommendations={result.recommendations} />
            </div>
          )}

          {activeTab === 'ai-insights' && (
            <AIInsightsSection 
              readinessScore={result.readiness_score}
              recommendations={result.recommendations}
              executiveSummary={result.executive_summary}
            />
          )}

          {activeTab === 'exchange' && (
            <ExchangeRequirementsSection 
              requirements={result.exchange_requirements}
              proposalUrl={result.proposal_pdf_url}
            />
          )}

          {activeTab === 'bridges' && (
            <BridgeRoutesSection 
              routes={result.bridge_routes}
              recommendedChain={result.recommended_chain}
            />
          )}

          {activeTab === 'masumi' && (
            <MasumiLogsSection logs={result.masumi_logs} />
          )}
        </div>
      </div>
    </div>
  )
}
