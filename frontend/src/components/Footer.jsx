function Footer() {
  return (
    <footer className="border-t border-slate-800 mt-16 py-8 bg-slate-900/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div>
            <h4 className="text-white font-semibold mb-2 text-sm">InfraGuard Studio</h4>
            <p className="text-slate-400 text-xs leading-relaxed">
              IaC dosyalarındaki güvenlik açıklarını anında tespit eden açık kaynak DevSecOps aracı.
            </p>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-2 text-sm">Teknolojiler</h4>
            <ul className="space-y-1 text-xs text-slate-400">
              <li>• React + Vite + Tailwind CSS</li>
              <li>• FastAPI + Python</li>
              <li>• Checkov (1000+ güvenlik kuralı)</li>
              <li>• Monaco Editor</li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-2 text-sm">Bağlantılar</h4>
            <ul className="space-y-1 text-xs">
              <li>
                <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors">GitHub Repository</a>
              </li>
              <li>
                <a href="https://www.checkov.io" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors">Checkov Dokümantasyonu</a>
              </li>
              <li>
                <a href="https://docs.docker.com/develop/develop-images/dockerfile_best-practices/" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 transition-colors">Dockerfile Best Practices</a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-3">
          <p className="text-xs text-slate-500">
            © 2026 Muhammed Asef · v1.0 • DevSecOps Portfolyo Projesi
          </p>
          <p className="text-xs text-slate-500">
            Yapım: <span className="text-cyan-400">React</span> + <span className="text-cyan-400">FastAPI</span>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer