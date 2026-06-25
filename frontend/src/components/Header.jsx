function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">InfraGuard Studio</h1>
            <p className="text-xs text-slate-400">IaC Security Auditor — Dockerfile, K8s & Terraform</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-sm">
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">
            GitHub
          </a>
          <span className="text-slate-600">|</span>
          <span className="text-slate-400">
            Powered by <span className="text-cyan-400 font-medium">Checkov</span>
          </span>
        </div>
      </div>
    </header>
  )
}

export default Header