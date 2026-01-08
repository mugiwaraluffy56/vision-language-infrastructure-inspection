import { useState, useRef } from 'react'
import './ImageUpload.css'

function ImageUpload({ onUpload }) {
  const [preview, setPreview] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef(null)

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleChange = (e) => {
    const file = e.target.files[0]
    handleFile(file)
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleSubmit = () => {
    const file = fileInputRef.current.files[0]
    if (file) {
      onUpload(file)
    }
  }

  const handleReset = () => {
    setPreview(null)
    fileInputRef.current.value = ''
  }

  return (
    <div className="upload-section">
      {!preview ? (
        <div
          className={`upload-area ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <div className="upload-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          </div>
          <h3>Upload Infrastructure Image</h3>
          <p>Drag and drop or click to select</p>
          <p className="supported-formats">Supports: JPG, PNG</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleChange}
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div className="preview-section">
          <img src={preview} alt="Preview" className="preview-image" />
          <div className="preview-actions">
            <button onClick={handleReset} className="btn-secondary">
              Choose Different Image
            </button>
            <button onClick={handleSubmit} className="btn-primary">
              Analyze Image
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageUpload
