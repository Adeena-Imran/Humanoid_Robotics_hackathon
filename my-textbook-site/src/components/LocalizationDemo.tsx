// my-textbook-site/src/components/LocalizationDemo.tsx

import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { Pose } from '../lib/robot-model';
import { estimateRobotPose2D } from '../services/localization-service';
import { simulateIMUData } from '../lib/sensor-utils';
import SensorDataViewer from './SensorDataViewer'; // FIXED

// Initial robot pose
const initialPose: Pose = {
  position: { x: 0, y: 0, z: 0 },
  orientation: { x: 0, y: 0, z: 0, w: 1 }
};

interface LocalizationDemoProps {}

const LocalizationDemo: React.FC<LocalizationDemoProps> = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [robotPose, setRobotPose] = useState<Pose>(initialPose);
  const [simulatedTime, setSimulatedTime] = useState(0);
  const [simulating, setSimulating] = useState(false);
  const [simulatedSensorData, setSimulatedSensorData] = useState<any[]>([]);

  const [linearVelX, setLinearVelX] = useState(0.1);
  const [linearVelY, setLinearVelY] = useState(0.0);
  const [angularVelZ, setAngularVelZ] = useState(0.0);

  const updateSimulation = useCallback(() => {
    setSimulatedTime(prev => prev + 0.1);

    const motionData = {
      linearVelocity: { x: linearVelX, y: linearVelY, z: 0 }, // FIXED
      angularVelocityZ: angularVelZ,
    };

    const newImuData = simulateIMUData(
      { x: linearVelX / 0.1, y: linearVelY / 0.1, z: 0 },
      { x: 0, y: 0, z: angularVelZ },
      0.02, 0.005
    );

    setSimulatedSensorData(prev => [...prev, newImuData].slice(-10));

    const newPose = estimateRobotPose2D(robotPose, motionData);
    setRobotPose(newPose);
  }, [robotPose, linearVelX, linearVelY, angularVelZ]);

  useEffect(() => {
    let animationFrameId: number;
    let intervalId: NodeJS.Timeout;

    if (simulating) {
      intervalId = setInterval(() => {
        animationFrameId = requestAnimationFrame(updateSimulation);
      }, 100);
    }

    return () => {
      cancelAnimationFrame(animationFrameId);
      clearInterval(intervalId);
    };
  }, [simulating, updateSimulation]);

  const THREE = useMemo(() => require('three'), []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const gridSize = 1.0;
    const scale = 50;
    const center = { x: canvas.width / 2, y: canvas.height / 2 };

    ctx.strokeStyle = '#333';
    ctx.lineWidth = 0.5;

    for (let i = -5; i <= 5; i++) {
      ctx.beginPath();
      ctx.moveTo(center.x + i * gridSize * scale, 0);
      ctx.lineTo(center.x + i * gridSize * scale, canvas.height);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, center.y + i * gridSize * scale);
      ctx.lineTo(canvas.width, center.y + i * gridSize * scale);
      ctx.stroke();
    }

    const robotSize = 0.3 * scale;
    const robotX = center.x + robotPose.position.x * scale;
    const robotY = center.y - robotPose.position.y * scale;

    const euler = new THREE.Euler().setFromQuaternion(
      new THREE.Quaternion(
        robotPose.orientation.x,
        robotPose.orientation.y,
        robotPose.orientation.z,
        robotPose.orientation.w
      )
    );

    ctx.save();
    ctx.translate(robotX, robotY);
    ctx.rotate(-euler.z);

    ctx.beginPath();
    ctx.moveTo(robotSize / 2, 0);
    ctx.lineTo(-robotSize / 2, -robotSize / 2);
    ctx.lineTo(-robotSize / 2, robotSize / 2);
    ctx.closePath();
    ctx.fillStyle = 'blue';
    ctx.fill();
    ctx.strokeStyle = 'darkblue';
    ctx.stroke();
    ctx.restore();

  }, [robotPose, simulatedTime, THREE]);

  return (
    <div style={{ display: 'flex', flexDirection:'column', alignItems:'center', width:'100%' }}>
      <div style={{ display: 'flex', gap:'20px', marginBottom:'20px' }}>
        <button onClick={() => setSimulating(prev => !prev)}>
          {simulating ? 'Pause Simulation' : 'Start Simulation'}
        </button>
        <button onClick={() => { setRobotPose(initialPose); setSimulatedTime(0); setSimulatedSensorData([]); setSimulating(false); }}>
          Reset
        </button>
      </div>

      <div style={{ display: 'flex', gap:'20px', flexWrap:'wrap', width:'100%' }}>
        <div style={{ flex: '1 1 500px', border: '1px solid gray' }}>
          <canvas ref={canvasRef} width="500" height="500" style={{ background:'#000' }}></canvas>
        </div>

        <div style={{ maxWidth:'300px' }}>
          <h3>Motion Controls</h3>

          <label>
            Linear X: {linearVelX.toFixed(2)} m/s
            <input type="range" min={-0.5} max={0.5} step={0.01} value={linearVelX}
              onChange={e => setLinearVelX(parseFloat(e.target.value))}
            />
          </label>

          <label>
            Linear Y: {linearVelY.toFixed(2)} m/s
            <input type="range" min={-0.5} max={0.5} step={0.01} value={linearVelY}
              onChange={e => setLinearVelY(parseFloat(e.target.value))}
            />
          </label>

          <label>
            Angular Z: {angularVelZ.toFixed(2)} rad/s
            <input type="range" min={-1} max={1} step={0.01} value={angularVelZ}
              onChange={e => setAngularVelZ(parseFloat(e.target.value))}
            />
          </label>

          <SensorDataViewer sensorData={simulatedSensorData} title="Simulated IMU Data" />
        </div>
      </div>
    </div>
  );
};

export default LocalizationDemo;

