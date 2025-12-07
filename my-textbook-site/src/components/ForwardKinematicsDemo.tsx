// my-textbook-site/src/components/ForwardKinematicsDemo.tsx

import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three'; // Import THREE for matrix, vector, quaternion operations

import RobotScene from './RobotScene';
import { HumanoidRobotModel, Link, Joint, Pose, Vector3, Quaternion } from '../lib/robot-model';
import { createVector3, createQuaternion, createPose, addVectors, transformPose } from '../lib/coordinate-frames';
import { calculateForwardKinematics } from '../services/forward-kinematics';

// Dummy Robot Model for visualization
const dummyRobotModel: HumanoidRobotModel = {
  id: 'dummyRobot',
  name: 'Dummy 2-DOF Arm',
  baseLinkId: 'baseLink',
  links: [
    { id: 'baseLink', name: 'Base' },
    { id: 'link1', name: 'Link 1' },
    { id: 'link2', name: 'Link 2' },
    { id: 'endEffectorLink', name: 'End Effector Link' }, // Separate link for visualization of end effector
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

interface ForwardKinematicsDemoProps {
  // No specific props yet, but can be added later
}

/**
 * RobotArm component visualizes a simplified 2-DOF robotic arm based on joint angles.
 */
const RobotArm: React.FC<{
  robotModel: HumanoidRobotModel;
  jointAngles: Map<string, number>;
  endEffectorPose: Pose | null;
}> = ({ robotModel, jointAngles, endEffectorPose }) => {

  const linkLength = 1.0; // Assume unit length for links
  const linkRadius = 0.1; // Radius for visualization

  // Basic representation of the robot arm
  // This is a simplified direct visualization for a 2-DOF arm
  // A proper implementation would parse URDF/kinematic structure and build a hierarchy
  return (
    <group>
      {/* Base Link */}
      <mesh position={[0, -linkLength/2, 0]}>
        <boxGeometry args={[0.5, 0.5, 0.5]} />
        <meshStandardMaterial color="gray" />
      </mesh>

      {/* Joint 1 (Shoulder) and Link 1 */}
      {/* Position of Link 1 relative to base, rotated by joint1 angle */}
      <group rotation-z={jointAngles.get('joint1') || 0}>
        <mesh position={[0, linkLength / 2, 0]}>
          <boxGeometry args={[linkRadius * 2, linkLength, linkRadius * 2]} />
          <meshStandardMaterial color="hotpink" />
        </mesh>

        {/* Joint 2 (Elbow) and Link 2 */}
        {/* Position of Link 2 relative to Link 1, rotated by joint2 angle */}
        <group position={[0, linkLength, 0]} rotation-y={jointAngles.get('joint2') || 0}>
          <mesh position={[0, linkLength / 2, 0]}>
            <boxGeometry args={[linkRadius * 2, linkLength, linkRadius * 2]} />
            <meshStandardMaterial color="lightblue" />
          </mesh>

          {/* End Effector Visualization */}
          {endEffectorPose && (
            <mesh position={[0, linkLength, 0]} castShadow>
                <sphereGeometry args={[linkRadius * 1.5, 16, 16]} />
                <meshStandardMaterial color="red" />
            </mesh>
          )}
        </group>
      </group>
    </group>
  );
};


/**
 * ForwardKinematicsDemo component provides an interactive demonstration of forward kinematics.
 * It displays a 2-DOF robotic arm, allows manipulation of joint angles via sliders,
 * and visualizes the calculated end-effector pose in a 3D scene.
 */
const ForwardKinematicsDemo: React.FC<ForwardKinematicsDemoProps> = () => {
  const [joint1Angle, setJoint1Angle] = useState(0); // Shoulder Yaw
  const [joint2Angle, setJoint2Angle] = useState(0); // Elbow Pitch

  const jointAnglesMap = useMemo(() => {
    const map = new Map<string, number>();
    map.set('joint1', joint1Angle);
    map.set('joint2', joint2Angle);
    return map;
  }, [joint1Angle, joint2Angle]);

  // Recalculate FK pose
  const endEffectorPose = useMemo(() => {
    // This calls the placeholder FK service
    return calculateForwardKinematics(
      dummyRobotModel,
      jointAnglesMap,
      'endEffector'
    );
  }, [jointAnglesMap]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ width: '100%', height: '50vh', background: '#222' }}>
        <RobotScene>
          <RobotArm robotModel={dummyRobotModel} jointAngles={jointAnglesMap} endEffectorPose={endEffectorPose} />
        </RobotScene>
      </div>

      <div style={{ marginTop: '20px', width: '80%', maxWidth: '600px' }}>
        <h3>Joint Controls</h3>
        <div>
          <label>
            Joint 1 (Shoulder Yaw): {joint1Angle.toFixed(2)} rad ({ (joint1Angle * 180 / Math.PI).toFixed(1) }°)
            <input
              type="range"
              min={-Math.PI / 2}
              max={Math.PI / 2}
              step={0.01}
              value={joint1Angle}
              onChange={(e) => setJoint1Angle(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <div>
          <label>
            Joint 2 (Elbow Pitch): {joint2Angle.toFixed(2)} rad ({ (joint2Angle * 180 / Math.PI).toFixed(1) }°)
            <input
              type="range"
              min={-Math.PI / 2}
              max={Math.PI / 2}
              step={0.01}
              value={joint2Angle}
              onChange={(e) => setJoint2Angle(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>
        {endEffectorPose && (
          <div style={{ marginTop: '10px' }}>
            <h4>End Effector Pose (FK Result - Placeholder)</h4>
            <p>Position: X: {endEffectorPose.position.x.toFixed(2)}, Y: {endEffectorPose.position.y.toFixed(2)}, Z: {endEffectorPose.position.z.toFixed(2)}</p>
            {/* Orientation could also be displayed */}
          </div>
        )}
      </div>
    </div>
  );
};

export default ForwardKinematicsDemo;
