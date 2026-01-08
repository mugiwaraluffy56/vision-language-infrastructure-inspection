import './InspectionReport.css'

function InspectionReport({ result, onReset }) {
  const getSeverityClass = (severity) => {
    return `severity-${severity.toLowerCase()}`
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'High':
        return '⚠️'
      case 'Medium':
        return '⚡'
      case 'Low':
        return 'ℹ️'
      default:
        return '•'
    }
  }

  return (
    <div className="report-section">
      <div className="report-header">
        <h2>Inspection Report</h2>
        <button onClick={onReset} className="btn-secondary">
          New Inspection
        </button>
      </div>

      <div className="summary-card">
        <h3>Summary</h3>
        <p>{result.summary}</p>
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-label">Total Defects</span>
            <span className="stat-value">{result.total_defects}</span>
          </div>
        </div>
      </div>

      {result.detections && result.detections.length > 0 && (
        <div className="detections-container">
          <h3>Detected Defects</h3>
          {result.detections.map((detection, index) => (
            <div key={index} className="detection-card">
              <div className="detection-header">
                <div className="defect-info">
                  <h4>
                    {detection.defect_type.charAt(0).toUpperCase() + detection.defect_type.slice(1)}
                  </h4>
                  <span className="confidence">
                    Confidence: {(detection.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className={`severity-badge ${getSeverityClass(detection.severity)}`}>
                  <span className="severity-icon">{getSeverityIcon(detection.severity)}</span>
                  <span>{detection.severity} Severity</span>
                </div>
              </div>

              <div className="detection-content">
                <div className="detail-section">
                  <h5>Analysis</h5>
                  <p>{detection.explanation}</p>
                </div>

                <div className="detail-section">
                  <h5>Severity Assessment</h5>
                  <p>{detection.severity_reasoning}</p>
                </div>

                <div className="detail-section recommended">
                  <h5>Recommended Action</h5>
                  <p>{detection.recommended_action}</p>
                </div>

                <div className="detail-section location">
                  <h5>Location</h5>
                  <div className="bbox-info">
                    <span>X: {Math.round(detection.bounding_box.x1)} - {Math.round(detection.bounding_box.x2)}</span>
                    <span>Y: {Math.round(detection.bounding_box.y1)} - {Math.round(detection.bounding_box.y2)}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {result.detections && result.detections.length === 0 && (
        <div className="no-detections">
          <p>No structural defects detected in the image.</p>
          <p className="sub-text">The analyzed infrastructure appears to be in good condition.</p>
        </div>
      )}
    </div>
  )
}

export default InspectionReport
