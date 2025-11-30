'use client'

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { Download, RefreshCw, Award, Activity, FileText, ChevronDown, Zap, CheckCircle } from 'lucide-react'
import ScoreCard from './ScoreCard'
import MetricsSection from './MetricsSection'
import RecommendationsSection from './RecommendationsSection'
import ExchangeRequirementsSection from './ExchangeRequirementsSection'
import BridgeRoutesSection from './BridgeRoutesSection'
import MasumiLogsSection from './MasumiLogsSection'
import AIInsightsSection from './AIInsightsSection'
import EmailReportModal from './EmailReportModal'

interface ResultsDashboardProps {
  result: any
  onNewAnalysis: () => void
}

export default function ResultsDashboard({ result, onNewAnalysis }: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview')
  const [isExporting, setIsExporting] = useState(false)
  // email modal removed per user request
  const [showViewDropdown, setShowViewDropdown] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowViewDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const tabs = [
    { id: 'overview', label: 'OVERVIEW', icon: '📊' },
    { id: 'ai-insights', label: 'AI INSIGHTS', icon: '🤖' },
    { id: 'exchange', label: 'EXCHANGE', icon: '🏦' },
    { id: 'bridges', label: 'BRIDGES', icon: '🌉' },
    { id: 'masumi', label: 'AUDIT LOG', icon: '📝' },
  ]

  const handleExportPDF = async () => {
    setIsExporting(true)
    try {
      const response = await axios.post(
        'http://localhost:8000/api/export/pdf',
        result,
        { responseType: 'blob' }
      )

      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      window.open(url, '_blank')
      
      setTimeout(() => {
        window.URL.revokeObjectURL(url)
      }, 100)
    } catch (error) {
      console.error('Error exporting PDF:', error)
      alert('Failed to export PDF. Please try again.')
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-6xl mx-auto space-y-6"
    >
      {/* Success Banner */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="pixel-card p-6 bg-gradient-to-r from-green-900/50 to-emerald-900/50 border-green-500"
      >
        <div className="flex items-center gap-4">
          <motion.div
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 2, ease: "easeInOut", repeat: Infinity }}
            className="w-12 h-12 bg-green-600 border-2 border-green-400 flex items-center justify-center"
          >
            <CheckCircle className="w-8 h-8 text-white" />
          </motion.div>
          <div>
            <p className="font-press-start text-sm text-green-400 mb-2">ANALYSIS COMPLETE</p>
            <p className="font-vt323 text-xl text-green-300">ECOSYSTEMBRIDGE AI PROCESSING SUCCESSFUL</p>
          </div>
        </div>
      </motion.div>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="pixel-card p-6"
      >
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-4 mb-3">
              <h1 className="text-3xl font-press-start text-white uppercase">
                {result.token_name}
              </h1>
              <span className="pixel-tag bg-blue-600 border-blue-400 text-white text-lg px-4 py-2">
                {result.token_symbol}
              </span>
            </div>
            <div className="font-vt323 text-lg text-slate-400 flex items-center gap-2 border-l-4 border-blue-500 pl-4 bg-slate-900/50 py-2">
              <Zap className="w-4 h-4 text-yellow-400" />
              POLICY: {result.policy_id.slice(0, 24)}...{result.policy_id.slice(-12)}
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleExportPDF}
              disabled={isExporting}
              className="pixel-btn pixel-btn-primary flex items-center gap-2"
            >
              <FileText className="w-4 h-4" />
              {isExporting ? 'LOADING...' : 'VIEW PDF'}
            </button>

            {/* Email feature removed */}

            <button
              onClick={onNewAnalysis}
              className="pixel-btn hover:bg-slate-700 flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              NEW
            </button>
          </div>
        </div>
      </motion.div>

      {/* Score Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <ScoreCard score={result.readiness_score} />
      </motion.div>

      {/* Executive Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="pixel-card p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-press-start text-lg text-white flex items-center gap-3">
            <Activity className="w-6 h-6 text-blue-400" />
            EXECUTIVE SUMMARY
          </h2>
          <motion.span
            className="pixel-tag bg-blue-600 border-blue-400 text-white text-xs"
            animate={{ opacity: [1, 0.7, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            AI GENERATED
          </motion.span>
        </div>
        <div
          className="font-vt323 text-xl leading-relaxed text-slate-300 bg-slate-900/50 p-6 border-l-4 border-blue-500"
          dangerouslySetInnerHTML={{ __html: result.executive_summary.replace(/\n/g, '<br />') }}
        />
      </motion.div>

      {/* Next Steps */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="pixel-card p-6 bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-500"
      >
        <h2 className="font-press-start text-lg text-white mb-6 flex items-center gap-3">
          <Award className="w-6 h-6 text-yellow-400" />
          RECOMMENDED NEXT STEPS
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {result.next_steps.map((step: string, index: number) => {
            let content = step;
            let priority = 'normal';
            if (content.startsWith('[HIGH]')) { priority = 'high'; content = content.replace('[HIGH]', '').trim(); }
            else if (content.startsWith('[MEDIUM]')) { priority = 'medium'; content = content.replace('[MEDIUM]', '').trim(); }
            else if (content.startsWith('[EXCHANGE]')) { priority = 'exchange'; content = content.replace('[EXCHANGE]', '').trim(); }

            const parts = content.split(/(\*\*.*?\*\*)/g);

            let badgeColor = "bg-blue-600 border-blue-400";
            if (priority === 'high') badgeColor = "bg-red-600 border-red-400";
            if (priority === 'exchange') badgeColor = "bg-purple-600 border-purple-400";
            if (priority === 'medium') badgeColor = "bg-yellow-600 border-yellow-400";

            return (
              <motion.div
                key={index}
                className="bg-slate-900/50 p-4 border-2 border-slate-700 flex items-start gap-4 hover:border-slate-600 transition-colors"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
              >
                <div className={`flex-shrink-0 w-10 h-10 ${badgeColor} border-2 flex items-center justify-center font-press-start text-white text-sm`}>
                  {index + 1}
                </div>
                <div>
                  <p className="font-vt323 text-lg text-slate-200 leading-snug">
                    {parts.map((part, i) => (
                      part.startsWith('**') && part.endsWith('**')
                        ? <strong key={i} className="text-white font-bold">{part.slice(2, -2)}</strong>
                        : <span key={i}>{part}</span>
                    ))}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="pixel-card overflow-hidden"
      >
        {/* Tab Headers */}
        <div className="border-b-4 border-slate-700 bg-slate-900/50 p-2">
          <div className="flex gap-2 overflow-x-auto">
            {tabs.map((tab, i) => (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 font-press-start text-xs whitespace-nowrap transition-all border-2 ${activeTab === tab.id
                    ? 'bg-blue-600 border-blue-400 text-white shadow-[4px_4px_0px_0px_#000033]'
                    : 'bg-slate-800 border-slate-600 text-slate-400 hover:bg-slate-700'
                  }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + i * 0.05 }}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          <AnimatePresence mode="wait">
            {activeTab === 'overview' && (
              <motion.div
                key="overview"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="space-y-8"
              >
                <MetricsSection metrics={result.metrics} />
              </motion.div>
            )}

            {activeTab === 'ai-insights' && (
              <motion.div
                key="ai-insights"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <AIInsightsSection
                  readinessScore={result.readiness_score}
                  recommendations={result.recommendations}
                  executiveSummary={result.executive_summary}
                  policyId={result.policy_id}
                />
              </motion.div>
            )}

            {activeTab === 'exchange' && (
              <motion.div
                key="exchange"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <ExchangeRequirementsSection
                  requirements={result.exchange_requirements}
                  proposalUrl={result.proposal_pdf_url}
                />
              </motion.div>
            )}

            {activeTab === 'bridges' && (
              <motion.div
                key="bridges"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <BridgeRoutesSection
                  routes={result.bridge_routes}
                  recommendedChain={result.recommended_chain}
                />
              </motion.div>
            )}

            {activeTab === 'masumi' && (
              <motion.div
                key="masumi"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <MasumiLogsSection logs={result.masumi_logs} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Email report feature removed */}
    </motion.div>
  )
}
