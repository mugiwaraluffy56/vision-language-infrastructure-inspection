import { useState } from 'react'
import axios from 'axios'
import ImageUpload from './components/ImageUpload'
import InspectionReport from './components/InspectionReport'
import './App.css'

function App() {
  const [inspectionResult, setInspectionResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleImageUpload = async (file) => {
    setLoading(true)
    setError(null)
    setInspectionResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/inspect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setInspectionResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process image. Please try again.')
      console.error('Inspection error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setInspectionResult(null)
    setError(null)
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Infrastructure Inspection System</h1>
          <p>AI-powered structural defect detection and analysis</p>
        </header>

        {!inspectionResult && !loading && (
          <ImageUpload onUpload={handleImageUpload} />
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing image...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <h3>Error</h3>
            <p>{error}</p>
            <button onClick={handleReset} className="btn-secondary">
              Try Again
            </button>
          </div>
        )}

        {inspectionResult && !loading && (
          <InspectionReport result={inspectionResult} onReset={handleReset} />
        )}
      </div>
    </div>
  )
}

export default App
