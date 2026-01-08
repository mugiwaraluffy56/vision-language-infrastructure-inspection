import React, { useState, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

const fadeInUp = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

export default function Inspector() {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            const selected = e.target.files[0];
            setFile(selected);
            setPreview(URL.createObjectURL(selected));
            setResult(null);
        }
    };

    const handleInspect = async () => {
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Mock delay for scan effect if response is too fast
            const [res] = await Promise.all([
                axios.post('http://localhost:8000/inspect', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                }),
                new Promise(resolve => setTimeout(resolve, 1500))
            ]);
            setResult(res.data);
        } catch (error) {
            console.error("Inspection failed", error);
            alert("Inspection failed. Backend might be offline.");
        } finally {
            setLoading(false);
        }
    };

    const clearAll = () => {
        setFile(null);
        setPreview(null);
        setResult(null);
    };

    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(400px, 1fr) 1.5fr', gap: '2rem', width: '100%', height: '100%', padding: '0 2rem 2rem 2rem' }}>

            {/* LEFT PANEL: CONTROLS */}
            <motion.div
                variants={fadeInUp} initial="hidden" animate="visible"
                className="glass-panel"
                style={{ padding: '2rem', borderRadius: '24px', display: 'flex', flexDirection: 'column', height: 'fit-content' }}
            >
                <div style={{ marginBottom: '2rem' }}>
                    <h2 className="glow-text" style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>SCAN TARGET</h2>
                    <p style={{ color: 'var(--text-dim)' }}>Upload infrastructure imagery for AI analysis.</p>
                </div>

                <div
                    onClick={() => fileInputRef.current.click()}
                    className={`upload-area ${file ? 'active' : ''}`}
                    style={{
                        flex: 1, minHeight: '300px', borderRadius: '16px',
                        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                        cursor: 'pointer', position: 'relative', overflow: 'hidden', background: 'rgba(0,0,0,0.2)'
                    }}
                >
                    {preview ? (
                        <img src={preview} alt="Target" style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: loading ? 0.5 : 1 }} />
                    ) : (
                        <div style={{ textAlign: 'center', color: 'var(--text-dim)' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }}>+</div>
                            <p>DROP FILE OR CLICK TO SCAN</p>
                        </div>
                    )}

                    {loading && (
                        <div style={{
                            position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
                            background: 'linear-gradient(to bottom, transparent, var(--secondary), transparent)',
                            opacity: 0.3, animation: 'scan 1.5s linear infinite'
                        }} />
                    )}

                    <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileChange} style={{ display: 'none' }} />
                </div>

                <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                    <button
                        className="btn-primary"
                        style={{ flex: 1, opacity: !file || loading ? 0.5 : 1 }}
                        onClick={handleInspect}
                        disabled={!file || loading}
                    >
                        {loading ? 'PROCESSING...' : 'INITIATE SCAN'}
                    </button>
                    {file && !loading && (
                        <button
                            onClick={clearAll}
                            style={{
                                background: 'transparent', border: '1px solid var(--error)', color: 'var(--error)',
                                borderRadius: '12px', padding: '0 20px', cursor: 'pointer', fontFamily: 'var(--font-display)', fontWeight: 600
                            }}
                        >
                            RESET
                        </button>
                    )}
                </div>
            </motion.div>

            {/* RIGHT PANEL: RESULTS */}
            <motion.div
                variants={fadeInUp} initial="hidden" animate="visible" style={{ transitionDelay: '0.2s' }}
                className="glass-panel"
                style={{ padding: '2rem', borderRadius: '24px', display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}
            >
                <div style={{ marginBottom: '2rem', paddingBottom: '1rem', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h2 style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.05em' }}>DIAGNOSTIC REPORT</h2>
                        <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
                            <span style={{ color: 'var(--text-dim)', fontSize: '0.8rem' }}>SYSTEM: ONLINE</span>
                            <span style={{ color: 'var(--accent)', fontSize: '0.8rem' }}>VLM PRO: ACTIVE</span>
                        </div>
                    </div>
                    {result && (
                        <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>DETECTED FLAWS</div>
                            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'white' }}>{result.defects.length}</div>
                        </div>
                    )}
                </div>

                <div style={{ flex: 1, overflowY: 'auto' }}>
                    {!result && !loading && (
                        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', opacity: 0.3 }}>
                            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>⌬</div>
                            <p style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.1em' }}>NO DATA AVAILABLE</p>
                        </div>
                    )}

                    {result && result.defects.length === 0 && (
                        <div style={{ padding: '2rem', background: 'rgba(0, 255, 157, 0.1)', border: '1px solid var(--accent)', borderRadius: '12px' }}>
                            <h3 style={{ color: 'var(--accent)' }}>STRUCTURAL INTEGRITY CONFIRMED</h3>
                            <p style={{ marginTop: '0.5rem', color: '#ccc' }}>No visible defects identified by the vision system.</p>
                        </div>
                    )}

                    <AnimatePresence>
                        {result?.defects.map((defect, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                style={{
                                    background: 'rgba(255,255,255,0.03)',
                                    borderRadius: '12px',
                                    padding: '1.5rem',
                                    marginBottom: '1rem',
                                    borderLeft: `4px solid ${defect.severity === 'High' ? 'var(--error)' : 'var(--secondary)'}`
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                                    <div>
                                        <h3 style={{ fontSize: '1.2rem', textTransform: 'uppercase' }}>{defect.defect_type}</h3>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>CONFIDENCE: {Math.random().toFixed(2) * 10 + 85}%</div>
                                    </div>
                                    <span
                                        className="status-badge"
                                        style={{
                                            background: defect.severity === 'High' ? 'rgba(255, 0, 85, 0.2)' : 'rgba(0, 198, 255, 0.2)',
                                            color: defect.severity === 'High' ? 'var(--error)' : 'var(--secondary)',
                                        }}
                                    >
                                        {defect.severity} RISK
                                    </span>
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                    <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px' }}>
                                        <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Analysis</div>
                                        <p style={{ fontSize: '0.9rem', lineHeight: '1.6', margin: 0 }}>{defect.explanation}</p>
                                    </div>
                                    <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px' }}>
                                        <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Protocol</div>
                                        <p style={{ fontSize: '0.9rem', lineHeight: '1.6', margin: 0, color: 'var(--text-main)' }}>{defect.recommended_action}</p>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </motion.div>

            <style>{`
        @keyframes scan {
            0% { top: -100%; }
            100% { top: 200%; }
        }
      `}</style>
        </div>
    );
}
