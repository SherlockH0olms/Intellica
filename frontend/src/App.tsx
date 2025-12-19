import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState<string>('checking...')

  useEffect(() => {
    // Check backend connection
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => {
        setBackendStatus(`Connected: ${data.message}`)
      })
      .catch(() => {
        setBackendStatus('Backend not available')
      })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏭 Intellica</h1>
        <h2>AI-Powered Sənaye Optimallaşma Platforması</h2>
        <p className="status">Backend Status: {backendStatus}</p>
        <div className="features">
          <div className="feature-card">
            <h3>🤖 Anomaliya Detection</h3>
            <p>Real-vaxt sensor monitorinqi və anomaliya aşkarlama</p>
          </div>
          <div className="feature-card">
            <h3>🔮 Predictive Maintenance</h3>
            <p>7 gün qabaqcadan nasazlıq proqnozu</p>
          </div>
          <div className="feature-card">
            <h3>📊 Konfiqurasiya Optimallaşdırma</h3>
            <p>AI əsaslı avtomatik parametr tövsiyələri</p>
          </div>
          <div className="feature-card">
            <h3>👁️ Defekt Detection</h3>
            <p>Computer Vision ilə məhsul qusurlarının aşkarlanması</p>
          </div>
        </div>
      </header>
    </div>
  )
}

export default App