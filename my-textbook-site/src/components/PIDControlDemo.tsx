// my-textbook-site/src/components/PIDControlDemo.tsx

import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { PIDController } from '../services/pid-controller';
import { eulerIntegrate1D, simulateSingleJointPhysics } from '../lib/physics-utils';
import ControlSystemViewer from './ControlSystemViewer';

interface PIDControlDemoProps {}

const SIMULATION_TIMESTEP = 0.01; // seconds

/**
 * PIDControlDemo component provides an interactive simulation of a single-joint system
 * controlled by a PID controller. Users can tune Kp, Ki, and Kd gains and observe
 * the system's response to a setpoint change, visualized in a chart.
 */
const PIDControlDemo: React.FC<PIDControlDemoProps> = () => {
  // PID Gains
  const [kp, setKp] = useState(10);
  const [ki, setKi] = useState(0);
  const [kd, setKd] = useState(0);

  // System State (e.g., a simple pendulum/motor joint)
  const [currentAngle, setCurrentAngle] = useState(0); // radians
  const [angularVelocity, setAngularVelocity] = useState(0); // rad/s
  const [setpoint, setSetpoint] = useState(Math.PI / 2); // Target angle: 90 degrees

  // Simulation History for Plotting
  const [timeHistory, setTimeHistory] = useState<number[]>([]);
  const [angleHistory, setAngleHistory] = useState<number[]>([]);
  const [errorHistory, setErrorHistory] = useState<number[]>([]);
  const [controlOutputHistory, setControlOutputHistory] = useState<number[]>([]);

  const pidControllerRef = useRef(new PIDController(kp, ki, kd, -100, 100)); // Max torque/force

  // Update PID controller parameters when gains change
  useEffect(() => {
    pidControllerRef.current.kp = kp;
    pidControllerRef.current.ki = ki;
    pidControllerRef.current.kd = kd;
  }, [kp, ki, kd]);

  // Reset simulation
  const resetSimulation = useCallback(() => {
    pidControllerRef.current.reset();
    setCurrentAngle(0);
    setAngularVelocity(0);
    setSimulatedTime(0);
    setTimeHistory([]);
    setAngleHistory([]);
    setErrorHistory([]);
    setControlOutputHistory([]);
  }, []);

  const [simulating, setSimulating] = useState(false);
  const simulatedTimeRef = useRef(0);

  const simulateStep = useCallback(() => {
    // Performance Optimization Notes for Simulation Logic:
    // - For complex physics, consider offloading to a Web Worker.
    // - Optimize numerical integration (e.g., Runge-Kutta instead of Euler for accuracy/stability).
    // - Avoid unnecessary state updates; batch if possible.
    // - Profile and identify bottlenecks in physics calculations.

    // Calculate control output
    const controlOutput = pidControllerRef.current.update(setpoint, currentAngle, SIMULATION_TIMESTEP);

    // Simulate physics of a single joint
    // Assume a simple system: moment of inertia = 1, damping = 0.5
    const { newAngle, newAngularVelocity } = simulateSingleJointPhysics(
      currentAngle,
      angularVelocity,
      controlOutput, // Applied torque
      1.0,           // Moment of inertia (simplified)
      0.5,           // Damping coefficient (simplified)
      SIMULATION_TIMESTEP
    );

    setCurrentAngle(newAngle);
    setAngularVelocity(newAngularVelocity);

    // Update history for plotting
    simulatedTimeRef.current += SIMULATION_TIMESTEP;
    setTimeHistory(prev => [...prev, simulatedTimeRef.current]);
    setAngleHistory(prev => [...prev, newAngle]);
    setErrorHistory(prev => [...prev, setpoint - newAngle]);
    setControlOutputHistory(prev => [...prev, controlOutput]);

  }, [currentAngle, angularVelocity, setpoint]);

  useEffect(() => {
    let animationFrameId: number;
    let intervalId: NodeJS.Timeout;

    if (simulating) {
      intervalId = setInterval(() => {
        animationFrameId = requestAnimationFrame(simulateStep);
      }, SIMULATION_TIMESTEP * 1000); // Convert s to ms
    }

    return () => {
      cancelAnimationFrame(animationFrameId);
      clearInterval(intervalId);
    };
  }, [simulating, simulateStep]);


  const plotData = useMemo(() => ({
    labels: timeHistory.map(t => t.toFixed(2)),
    datasets: [
      {
        label: 'Current Angle (rad)',
        data: angleHistory,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        fill: false,
      },
      {
        label: 'Setpoint (rad)',
        data: angleHistory.map(() => setpoint), // Constant setpoint line
        borderColor: 'rgb(255, 99, 132)',
        borderDash: [5, 5],
        fill: false,
      },
      {
        label: 'Error (rad)',
        data: errorHistory,
        borderColor: 'rgb(255, 205, 86)',
        tension: 0.1,
        fill: false,
        hidden: true, // Hide by default
      },
      {
        label: 'Control Output',
        data: controlOutputHistory,
        borderColor: 'rgb(54, 162, 235)',
        tension: 0.1,
        fill: false,
        hidden: true, // Hide by default
      }
    ],
  }), [timeHistory, angleHistory, errorHistory, controlOutputHistory, setpoint]);


  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>PID Control Simulation</h2>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', width: '100%', marginBottom: '20px', justifyContent: 'center' }}>
        {/* Simulation Controls */}
        <div>
          <h3>Simulation Controls</h3>
          <button onClick={() => setSimulating(prev => !prev)} style={{ marginRight: '10px' }}>
            {simulating ? 'Pause' : 'Start'} Simulation
          </button>
          <button onClick={resetSimulation}>Reset</button>
        </div>

        {/* PID Gain Controls */}
        <div style={{ minWidth: '250px' }}>
          <h3>PID Gains</h3>
          <div>
            <label>Kp: {kp.toFixed(2)}</label>
            <input type="range" min={0} max={100} step={0.1} value={kp} onChange={e => setKp(parseFloat(e.target.value))} style={{ width: '100%' }} />
          </div>
          <div>
            <label>Ki: {ki.toFixed(2)}</label>
            <input type="range" min={0} max={10} step={0.01} value={ki} onChange={e => setKi(parseFloat(e.target.value))} style={{ width: '100%' }} />
          </div>
          <div>
            <label>Kd: {kd.toFixed(2)}</label>
            <input type="range" min={0} max={10} step={0.01} value={kd} onChange={e => setKd(parseFloat(e.target.value))} style={{ width: '100%' }} />
          </div>
        </div>

        {/* System Setpoint */}
        <div style={{ minWidth: '250px' }}>
          <h3>System Setpoint</h3>
          <div>
            <label>Setpoint (rad): {setpoint.toFixed(2)} ({ (setpoint * 180 / Math.PI).toFixed(1) }°)</label>
            <input type="range" min={0} max={Math.PI} step={0.01} value={setpoint} onChange={e => setSetpoint(parseFloat(e.target.value))} style={{ width: '100%' }} />
          </div>
        </div>
      </div>

      {/* Control System Response Viewer */}
      <div style={{ width: '100%', maxWidth: '800px', height: '400px', marginTop: '20px' }}>
        <ControlSystemViewer data={plotData} title="System Response" />
      </div>

      <div style={{ marginTop: '20px' }}>
        <h4>Current State:</h4>
        <p>Angle: {currentAngle.toFixed(3)} rad ({ (currentAngle * 180 / Math.PI).toFixed(1) }°)</p>
        <p>Angular Velocity: {angularVelocity.toFixed(3)} rad/s</p>
      </div>
    </div>
  );
};

export default PIDControlDemo;
