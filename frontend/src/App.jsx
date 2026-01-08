import React, { useEffect } from 'react'
import ThreeBackground from './components/ThreeBackground'
import Inspector from './components/Inspector'
import Lenis from '@studio-freight/lenis'

function App() {
    useEffect(() => {
        // Lenis might not be needed if we don't scroll much, but good for polished feel
        const lenis = new Lenis({ duration: 1.2 })
        function raf(time) {
            lenis.raf(time)
            requestAnimationFrame(raf)
        }
        requestAnimationFrame(raf)
        return () => lenis.destroy()
    }, [])

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}>
            <ThreeBackground />

            {/* HEADER */}
            <header style={{
                padding: '1.5rem 3rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backdropFilter: 'blur(10px)',
                borderBottom: '1px solid rgba(255,255,255,0.05)',
                zIndex: 10
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ width: '12px', height: '12px', background: 'var(--accent)', borderRadius: '50%', boxShadow: '0 0 10px var(--accent)' }}></div>
                    <h1 style={{ fontSize: '1.5rem', letterSpacing: '-0.03em' }}>INFRASTRUCT<span style={{ fontWeight: 300, opacity: 0.7 }}>AI</span></h1>
                </div>
                <div style={{ fontFamily: 'var(--font-display)', fontSize: '0.9rem', opacity: 0.5, letterSpacing: '0.1em' }}>
                    V 1.0.0 • ENG MODE
                </div>
            </header>

            {/* MAIN CONTENT */}
            <main style={{ flex: 1, position: 'relative', zIndex: 10, overflow: 'hidden', paddingTop: '1rem' }}>
                <Inspector />
            </main>

        </div>
    )
}

export default App
