import React, { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Stars, Plane } from '@react-three/drei'
import * as THREE from 'three'

function MovingPlane() {
    const mesh = useRef()
    useFrame((state) => {
        mesh.current.position.z = (state.clock.elapsedTime * 2) % 10
    })
    return (
        <group rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]}>
            <Plane args={[100, 100, 20, 20]} ref={mesh}>
                <meshBasicMaterial wireframe color="#2a0a4e" transparent opacity={0.3} />
            </Plane>
            <gridHelper args={[100, 40, 0xff00ff, 0x2a0a4e]} position={[0, 0.1, 0]} rotation={[Math.PI / 2, 0, 0]} />
        </group>
    )
}

function Fog() {
    return <fog attach="fog" args={['#030014', 5, 30]} />
}

export default function ThreeBackground() {
    return (
        <div className="full-screen" style={{ position: 'fixed', zIndex: -1 }}>
            <Canvas camera={{ position: [0, 1, 10], fov: 75 }}>
                <color attach="background" args={['#030014']} />
                <Fog />
                <ambientLight intensity={1} />
                <MovingPlane />
                <Stars radius={100} depth={50} count={3000} factor={4} saturation={1} fade speed={1} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#00c6ff" />
            </Canvas>
            <div style={{
                position: 'absolute',
                top: 0, left: 0, width: '100%', height: '100%',
                background: 'radial-gradient(circle at 50% 50%, transparent 0%, #030014 90%)',
                pointerEvents: 'none'
            }} />
        </div>
    )
}
