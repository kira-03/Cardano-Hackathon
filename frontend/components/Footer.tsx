export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-24">
      <div className="container mx-auto px-4 py-12 max-w-7xl">
        <div className="grid md:grid-cols-2 gap-12 mb-8">
          <div>
            <h3 className="font-semibold text-slate-900 mb-3">About This Tool</h3>
            <p className="text-sm text-slate-600 leading-relaxed max-w-md">
              Multi-agent AI system for analyzing Cardano tokens and preparing exchange listing applications. Built with FastAPI, Next.js, and Blockfrost API.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-slate-900 mb-3">Important Notice</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Analysis and recommendations are for informational purposes only. This tool does not guarantee exchange listing approval.
            </p>
          </div>
        </div>
        <div className="pt-8 border-t border-slate-200">
          <p className="text-sm text-slate-500">Built for Cardano Blockchain Hackathon 2024</p>
        </div>
      </div>
    </footer>
  )
}
