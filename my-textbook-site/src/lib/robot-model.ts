// my-textbook-site/src/lib/robot-model.ts

/**
 * Represents a 3D vector.
 */
export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

/**
 * Represents a quaternion for 3D orientation.
 */
export interface Quaternion {
  x: number;
  y: number;
  z: number;
  w: number;
}

/**
 * Represents a 3D pose (position and orientation).
 */
export interface Pose {
  position: Vector3;
  orientation: Quaternion;
}

/**
 * Represents a rigid body segment of the robot's structure.
 */
export interface Link {
  id: string;
  name: string;
  // Simplified for now; could include geometry, mass_properties
  // parent_joint_id?: string; // Reference to parent Joint ID
  // child_joint_ids?: string[]; // References to child Joint IDs
}

/**
 * A connection between two Links that allows relative motion.
 */
export interface Joint {
  id: string;
  name: string;
  type: 'revolute' | 'prismatic';
  axis: Vector3; // Axis of rotation or translation
  limits?: { lower: number; upper: number }; // min/max angle or position
  parentLinkId: string;
  childLinkId: string;
  // default_angle_position?: number; // Default configuration
}

/**
 * A series of connected Links and Joints from a base to an End-Effector.
 */
export interface KinematicChain {
  id: string;
  name: string;
  baseLinkId: string; // ID of the base link of this chain
  endEffectorId: string; // ID of the end effector of this chain
  linkIds: string[]; // Ordered list of Link IDs in the chain
  jointIds: string[]; // Ordered list of Joint IDs in the chain
}

/**
 * The operational part of the robot that interacts with the environment.
 */
export interface EndEffector {
  id: string;
  name: string;
  attachedLinkId: string; // ID of the Link it is attached to
  localTransform: Pose; // Transform from attachedLinkId frame to EndEffector frame
}

/**
 * Represents the overall physical structure and kinematic properties of a humanoid robot.
 */
export interface HumanoidRobotModel {
  id: string;
  name: string;
  description?: string;
  baseLinkId: string; // ID of the base link
  links: Link[];
  joints: Joint[];
  kinematicChains: KinematicChain[];
  endEffectors: EndEffector[];
}

// ------------------------------------------------------
// Helper factory functions (needed by ActuatorTypesDemo)
// ------------------------------------------------------

export function createVector3(x: number, y: number, z: number): Vector3 {
  return { x, y, z };
}

export function createQuaternion(x: number, y: number, z: number, w: number): Quaternion {
  return { x, y, z, w };
}

export function createPose(position: Vector3, orientation: Quaternion): Pose {
  return { position, orientation };
}

