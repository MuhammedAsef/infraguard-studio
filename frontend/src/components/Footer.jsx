function Footer() {
  return (
    <footer className="border-t border-slate-800 mt-16 py-10 bg-slate-900/30 backdrop-blur">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-md flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4 text-white">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
              </div>
              <h4 className="text-white font-semibold text-sm">InfraGuard Studio</h4>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed">
              IaC dosyalarındaki güvenlik açıklarını anında tespit eden açık kaynak DevSecOps aracı.
            </p>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-3 text-sm">Teknolojiler</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 rounded-full bg-cyan-400"></span>
                React + Vite + Tailwind CSS
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 rounded-full bg-cyan-400"></span>
                FastAPI + Python 3.12
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 rounded-full bg-cyan-400"></span>
                Checkov (1000+ güvenlik kuralı)
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 rounded-full bg-cyan-400"></span>
                OpenAI GPT-4o-mini (AI fallback)
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-3 text-sm">Bağlantılar</h4>
            <ul className="space-y-1.5 text-xs">
              <li>
                <a href="https://github.com/MuhammedAsef/infraguard-studio" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  → GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://www.checkov.io" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  → Checkov Dokümantasyonu
                </a>
              </li>
              <li>
                <a href="https://docs.docker.com/develop/develop-images/dockerfile_best-practices/" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  → Dockerfile Best Practices
                </a>
              </li>
              <li>
                <a href="https://kubernetes.io/docs/concepts/security/pod-security-standards/" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  → Kubernetes Pod Security
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-3">
          <p className="text-xs text-slate-500">
            © 2026 <a href="https://muhammedasef.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors">Muhammed Asef</a> · v1.0 · DevSecOps Portfolyo Projesi
          </p>
          <p className="text-xs text-slate-500">
            Yapım: <span className="text-cyan-400">React</span> + <span className="text-cyan-400">FastAPI</span> + <span className="text-cyan-400">Checkov</span>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer