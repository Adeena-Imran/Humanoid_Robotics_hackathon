// my-textbook-site/src/components/InverseKinematicsDemo.tsx

import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

import RobotScene from './RobotScene';
import { HumanoidRobotModel, Link, Joint, Pose, Vector3, Quaternion } from '../lib/robot-model';
import { createVector3, createQuaternion, createPose, addVectors, transformPose } from '../lib/coordinate-frames';
import { solveInverseKinematics } from '../services/inverse-kinematics';
import { calculateForwardKinematics } from '../services/forward-kinematics'; // To verify IK solution

// Dummy Robot Model (same as FK demo for consistency)
const dummyRobotModel: HumanoidRobotModel = {
  id: 'dummyRobot',
  name: 'Dummy 2-DOF Arm',
  baseLinkId: 'baseLink',
  links: [
    { id: 'baseLink', name: 'Base' },
    { id: 'link1', name: 'Link 1' },
    { id: 'link2', name: 'Link 2' },
    { id: 'endEffectorLink', name: 'End Effector Link' },
  ],
  joints: [
    { id: 'joint1', name: 'Shoulder Yaw', type: 'revolute', axis: createVector3(0, 0, 1), parentLinkId: 'baseLink', childLinkId: 'link1', limits: { lower: -Math.PI / 2, upper: Math.PI / 2 } },
    { id: 'joint2', name: 'Elbow Pitch', type: 'revolute', axis: createVector3(0, 1, 0), parentLinkId: 'link1', childLinkId: 'link2', limits: { lower: -Math.PI / 2, upper: Math.PI / 2 } },
  ],
  kinematicChains: [
    {
      id: 'armChain',
      name: 'Arm Kinematic Chain',
      baseLinkId: 'baseLink',
      endEffector: { id: 'endEffector', name: 'Arm End Effector', attachedLinkId: 'endEffectorLink', localTransform: createPose(createVector3(0, 0.5, 0), createQuaternion(0, 0, 0, 1)) },
      linkIds: ['baseLink', 'link1', 'link2', 'endEffectorLink'],
      jointIds: ['joint1', 'joint2']
    }
  ],
  endEffectors: [
    { id: 'endEffector', name: 'Arm End Effector', attachedLinkId: 'endEffectorLink', localTransform: createPose(createVector3(0, 0.5, 0), createQuaternion(0, 0, 0, 1)) }
  ]
};

interface InverseKinematicsDemoProps {
  // No specific props yet
}

/**
 * RobotArmIK component visualizes a simplified 2-DOF robotic arm in its solved configuration.
 * It also provides visual feedback on whether an IK solution was found.
 */
const RobotArmIK: React.FC<{
  robotModel: HumanoidRobotModel;
  jointAngles: Map<string, number>;
  // targetPose: Pose; // Might not be needed directly for rendering the arm itself
  solutionFound: boolean;
}> = ({ robotModel, jointAngles, solutionFound }) => {

  const linkLength = 1.0; // Assume unit length for links
  const linkRadius = 0.1;

  // For visualizing the robot in its solved configuration
  // The actual end-effector position of the ARM (using FK with IK result)
  const actualEndEffectorPose = useMemo(() => {
    return calculateForwardKinematics(robotModel, jointAngles, 'endEffector');
  }, [robotModel, jointAngles]);


  return (
    <group>
      {/* Base Link */}
      <mesh position={[0, -linkLength/2, 0]}>
        <boxGeometry args={[0.5, 0.5, 0.5]} />
        <meshStandardMaterial color="gray" />
      </mesh>

      {/* Joint 1 (Shoulder) and Link 1 */}
      <group rotation-z={jointAngles.get('joint1') || 0}>
        <mesh position={[0, linkLength / 2, 0]}>
          <boxGeometry args={[linkRadius * 2, linkLength, linkRadius * 2]} />
          <meshStandardMaterial color={solutionFound ? "hotpink" : "darkred"} />
        </mesh>

        {/* Joint 2 (Elbow) and Link 2 */}
        <group position={[0, linkLength, 0]} rotation-y={jointAngles.get('joint2') || 0}>
          <mesh position={[0, linkLength / 2, 0]}>
            <boxGeometry args={[linkRadius * 2, linkLength, linkRadius * 2]} />
            <meshStandardMaterial color={solutionFound ? "lightblue" : "darkred"} />
          </mesh>

          {/* Actual End Effector Visualization (where the arm actually is) */}
          {actualEndEffectorPose && (
            <mesh
              position={[0, linkLength, 0]} // Position relative to Link 2
              castShadow
            >
              <sphereGeometry args={[linkRadius * 1.5, 16, 16]} />
              <meshStandardMaterial color={solutionFound ? "green" : "gray"} />
            </mesh>
          )}
        </group>
      </group>
    </group>
  );
};


/**
 * InverseKinematicsDemo component provides an interactive demonstration of inverse kinematics.
 * It displays a 2-DOF robotic arm, allows manipulation of a target end-effector pose via sliders,
 * and visualizes the calculated joint angles (if a solution is found) in a 3D scene.
 * It also indicates when a target is unreachable.
 */
const InverseKinematicsDemo: React.FC<InverseKinematicsDemoProps> = () => {
  const [targetPosX, setTargetPosX] = useState(1.0);
  const [targetPosY, setTargetPosY] = useState(1.0);
  const [targetPosZ, setTargetPosZ] = useState(0.0);

  // Target Pose (simplified orientation for now)
  const targetPose = useMemo(() => {
    return createPose(
      createVector3(targetPosX, targetPosY, targetPosZ),
      createQuaternion(0, 0, 0, 1) // Identity orientation
    );
  }, [targetPosX, targetPosY, targetPosZ]);

  const [ikSolution, setIkSolution] = useState<Map<string, number> | null>(null);

  const solutionFound = useMemo(() => ikSolution !== null, [ikSolution]);

  // Solve IK whenever target pose changes
  useMemo(() => {
    const solution = solveInverseKinematics(dummyRobotModel, targetPose, 'endEffector');
    setIkSolution(solution);
  }, [targetPose]);


  // Current joint angles from IK solution (or defaults if no solution)
  const currentJointAngles = useMemo(() => ikSolution || new Map<string, number>([['joint1', 0], ['joint2', 0]]), [ikSolution]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ width: '100%', height: '50vh', background: '#222' }}>
        <RobotScene>
          <RobotArmIK robotModel={dummyRobotModel} jointAngles={currentJointAngles} solutionFound={solutionFound} />
          {/* Target sphere */}
          <mesh position={[targetPosX, targetPosY, targetPosZ]}>
            <sphereGeometry args={[0.1, 16, 16]} />
            <meshStandardMaterial color={solutionFound ? "blue" : "red"} />
          </mesh>
        </RobotScene>
      </div>

      <div style={{ marginTop: '20px', width: '80%', maxWidth: '600px' }}>
        <h3>Target End-Effector Position</h3>
        <div>
          <label>
            Target X: {targetPosX.toFixed(2)}
            <input
              type="range"
              min={-2} max={2} step={0.01}
              value={targetPosX}
              onChange={(e) => setTargetPosX(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <div>
          <label>
            Target Y: {targetPosY.toFixed(2)}
            <input
              type="range"
              min={-2} max={2} step={0.01}
              value={targetPosY}
              onChange={(e) => setTargetPosY(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <div>
          <label>
            Target Z: {targetPosZ.toFixed(2)}
            <input
              type="range"
              min={-2} max={2} step={0.01}
              value={targetPosZ}
              onChange={(e) => setTargetPosZ(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <div style={{ marginTop: '10px' }}>
          <h4>IK Solution Status: {solutionFound ? "Found" : "No Solution / Unreachable"}</h4>
          {solutionFound && ikSolution && (
            <p>Joint 1: {currentJointAngles.get('joint1')?.toFixed(2)} rad, Joint 2: {currentJointAngles.get('joint2')?.toFixed(2)} rad</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default InverseKinematicsDemo;
