// my-textbook-site/src/lib/control-model.ts

import { Pose, Vector3, Quaternion } from './robot-model'; // Reusing from robot-model
import { Sensor } from './perception-model'; // Reusing Sensor from perception-model

/**
 * Represents a trajectory, extended with control-specific limits.
 * Reuses definition from robot-model.ts but adds velocity/acceleration limits.
 */
export interface Trajectory {
  id: string;
  name: string;
  type: 'JOINT_SPACE' | 'TASK_SPACE';
  points: { time: number; jointAngles?: Map<string, number>; pose?: Pose }[];
  duration: number;
  velocityLimits?: { jointId: string; maxVelocity: number }[]; // Max joint velocities
  accelerationLimits?: { jointId: string; maxAcceleration: number }[]; // Max joint accelerations
}

/**
 * Represents a component that converts energy into mechanical motion.
 */
export interface Actuator {
  id: string;
  name: string;
  type: 'MOTOR_DC' | 'MOTOR_BLDC' | 'HYDRAULIC' | 'PNEUMATIC' | 'SEA';
  specifications: { [key: string]: any }; // e.g., maxTorque, maxSpeed, gearRatio
  mountPoint: Pose; // Location and orientation on the robot
  controlledJointId: string; // ID of the Joint this actuator controls
}

/**
 * Represents a system that manages and regulates the behavior of other devices or systems.
 */
export interface Controller {
  id: string;
  name: string;
  type: 'PID' | 'STATE_SPACE' | 'INVERSE_DYNAMICS';
  targetSystemId: string; // ID of the Joint or KinematicChain it targets
  parameters: { [key: string]: any }; // e.g., Kp, Ki, Kd for PID
}

/**
 * The feedback mechanism used to maintain a desired system state.
 */
export interface ControlLoop {
  id: string;
  name: string;
  type: 'POSITION_CONTROL' | 'VELOCITY_CONTROL' | 'FORCE_CONTROL';
  setpoint: number | Pose; // Desired value (e.g., angle, velocity, pose)
  feedbackSensorId: string; // ID of the Sensor (from Module 3) providing feedback
  actuatorId: string; // ID of the Actuator whose input is adjusted
  controllerId: string; // ID of the Controller implementing the logic
}
