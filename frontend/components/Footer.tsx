import { motion } from 'framer-motion'
// Removed AISymbol import

export default function Footer() {
  return (
    <footer className="border-t-4 border-purple-500 mt-32 bg-slate-900/90 backdrop-blur-sm relative overflow-hidden">
      {/* Blockchain flow background */}
      <div className="absolute inset-0 blockchain-flow opacity-10" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 max-w-6xl relative z-10">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-8">
          {/* Brand Section */}
          <div className="max-w-sm">
            <div className="flex items-center gap-3 mb-4">
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="w-10 h-10 bg-purple-600 border-4 border-purple-400 flex items-center justify-center"
              >
                <span className="text-xl">⬢</span>
              </motion.div>
              <span className="font-press-start text-sm text-white">NAVIGATOR</span>
            </div>
            <p className="font-vt323 text-lg text-slate-400 leading-relaxed mb-4">
              INTELLIGENT ANALYSIS PLATFORM FOR CARDANO TOKEN TEAMS. BUILT WITH FASTAPI, NEXT.JS, AND BLOCKFROST.
            </p>

            {/* Tech Stack Badges */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="pixel-tag bg-blue-900 border-blue-600 text-blue-300 flex items-center gap-2">
                {/* Cardano SVG logo */}
                <svg width="18" height="18" viewBox="0 0 100 100" fill="currentColor" style={{ display: 'inline' }}>
                  <circle cx="50" cy="50" r="6" />
                  {Array.from({ length: 6 }).map((_, i) => {
                    const angle = (i * 60) * (Math.PI / 180);
                    const x = 50 + 18 * Math.cos(angle);
                    const y = 50 + 18 * Math.sin(angle);
                    return <circle key={i} cx={x} cy={y} r="3.5" />;
                  })}
                  {Array.from({ length: 12 }).map((_, i) => {
                    const angle = (i * 30) * (Math.PI / 180);
                    const x = 50 + 30 * Math.cos(angle);
                    const y = 50 + 30 * Math.sin(angle);
                    return <circle key={i+6} cx={x} cy={y} r="2.5" />;
                  })}
                  {Array.from({ length: 18 }).map((_, i) => {
                    const angle = (i * 20) * (Math.PI / 180);
                    const x = 50 + 40 * Math.cos(angle);
                    const y = 50 + 40 * Math.sin(angle);
                    return <circle key={i+18} cx={x} cy={y} r="1.8" />;
                  })}
                </svg>
                CARDANO
              </span>
              <span className="pixel-tag bg-purple-900 border-purple-600 text-purple-300">
                ⬢ MASUMI
              </span>
              <span className="pixel-tag bg-slate-800 border-slate-600 text-slate-300">
                {/* OpenAI stylized logo */}
                <span className="text-lg">👾</span>
                OPENAI
              </span>
            </div>
          </div>

          {/* Disclaimer Section */}
          <div className="pixel-card p-5 bg-slate-800/50 border-yellow-500 max-w-md">
            <p className="font-press-start text-xs text-yellow-400 mb-3">⚠️ DISCLAIMER</p>
            <p className="font-vt323 text-base text-slate-300 leading-relaxed">
              ANALYSIS AND RECOMMENDATIONS ARE FOR INFORMATIONAL PURPOSES ONLY.
              THIS TOOL DOES NOT GUARANTEE EXCHANGE LISTING APPROVAL.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
