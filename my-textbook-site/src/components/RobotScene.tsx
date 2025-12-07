// my-textbook-site/src/components/RobotScene.tsx

import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei'; // Commonly used for camera controls

interface RobotSceneProps {
  children?: React.ReactNode;
}

const Box = (props: any) => {
  // This is a placeholder for a robot link or component
  const meshRef = useRef<THREE.Mesh>(null!);
  useFrame(() => {
    meshRef.current.rotation.x += 0.01;
    meshRef.current.rotation.y += 0.01;
  });
  return (
    <mesh {...props} ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={'orange'} />
    </mesh>
  );
};

/**
 * RobotScene component sets up a basic 3D scene using @react-three/fiber.
 * It includes ambient light, point light, orbit controls, and axis helpers.
 * This component serves as the base for rendering 3D robot models and interactive elements.
 * Props:
 *   children: ReactNode - Any 3D objects or components to be rendered inside the scene.
 */
const RobotScene: React.FC<RobotSceneProps> = ({ children }) => {
  return (
    <Canvas
      style={{ width: '100%', height: '500px', background: '#222' }}
      camera={{ position: [5, 5, 5], fov: 75 }}
    >
      {/* Performance Optimization Notes:
          - Use useMemo/useCallback for expensive calculations or object creations.
          - Implement frustum culling for off-screen objects.
          - Optimize geometry (e.g., merge meshes, use instancing).
          - Use Web Workers for heavy computations to avoid blocking main thread.
          - Consider Level of Detail (LOD) for complex models.
      */}
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <OrbitControls /> {/* Allows user to rotate and zoom the scene */}
      <axesHelper args={[2]} /> {/* Shows X, Y, Z axes */}

      {/* Placeholder content for now */}
      <Box position={[0, 0, 0]} />

      {children}
    </Canvas>
  );
};

export default RobotScene;
