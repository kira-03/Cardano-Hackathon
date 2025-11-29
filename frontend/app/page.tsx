'use client'

import { useState } from 'react'
import AnalysisForm from '@/components/AnalysisForm'
import ResultsDashboard from '@/components/ResultsDashboard'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import AIStatusIndicator from '@/components/AIStatusIndicator'

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleAnalysisComplete = (result: any) => {
    setAnalysisResult(result)
    setIsLoading(false)
  }

  const handleNewAnalysis = () => {
    setAnalysisResult(null)
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <AIStatusIndicator />
      
      <main className="container mx-auto px-4 py-12 max-w-7xl">
        {!analysisResult ? (
          <div className="space-y-16">
            {/* Hero Section */}
            <div className="max-w-3xl">
              <div className="flex items-center gap-3 mb-4">
                <div className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  Cardano Token Analysis Platform
                </div>
                <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full text-xs font-bold shadow-md">
                  <span>🤖</span>
                  AI-POWERED
                  <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                </div>
              </div>
              <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 leading-tight">
                Get your token ready for
                <span className="text-blue-600"> exchange listings</span>
              </h1>
              <p className="text-lg text-slate-600 leading-relaxed">
                Comprehensive readiness analysis, automated proposal generation, and cross-chain expansion planning powered by <span className="font-semibold text-purple-600">Google Gemini 2.5 Flash AI</span> and multi-agent intelligence.
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid md:grid-cols-3 gap-6">
              <FeatureCard
                title="Readiness Scoring"
                description="Evaluate liquidity depth, holder distribution, and metadata completeness against exchange requirements"
              />
              <FeatureCard
                title="Proposal Generation"
                description="Professional PDF documents tailored to exchange application processes"
              />
              <FeatureCard
                title="Bridge Analysis"
                description="Compare cross-chain routes by cost, speed, and security for optimal expansion"
              />
            </div>

            {/* Analysis Form */}
            <div className="max-w-3xl">
              <AnalysisForm
                onAnalysisComplete={handleAnalysisComplete}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            </div>
          </div>
        ) : (
          <ResultsDashboard
            result={analysisResult}
            onNewAnalysis={handleNewAnalysis}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 border-l-4 border-blue-500 bg-white">
      <h3 className="text-lg font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-slate-600 text-sm leading-relaxed">{description}</p>
    </div>
  )
}
