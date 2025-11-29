export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200">
      <div className="container mx-auto px-4 py-4 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-blue-600 rounded flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-lg font-semibold text-slate-900">Navigator</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <a href="http://localhost:8000/docs" target="_blank" className="text-sm text-slate-600 hover:text-slate-900 transition-colors">
              API Docs
            </a>
            <a href="#" className="text-sm px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md transition-colors">
              Documentation
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}
