// my-textbook-site/src/lib/coordinate-frames.ts

import { Vector3, Quaternion, Pose } from './robot-model';

/**
 * Creates a new Vector3.
 */
export function createVector3(x: number, y: number, z: number): Vector3 {
  return { x, y, z };
}

/**
 * Creates a new Quaternion. (Assuming WXYZ order for convenience, but could be XYZW)
 */
export function createQuaternion(x: number, y: number, z: number, w: number): Quaternion {
  return { x, y, z, w };
}

/**
 * Creates a new Pose.
 */
export function createPose(position: Vector3, orientation: Quaternion): Pose {
  return { position, orientation };
}

/**
 * Performs a 3D vector addition.
 */
export function addVectors(v1: Vector3, v2: Vector3): Vector3 {
  return { x: v1.x + v2.x, y: v1.y + v2.y, z: v1.z + v2.z };
}

/**
 * Applies a rotation (from quaternion) to a vector.
 * Simplified example, a proper implementation would use quaternion multiplication.
 */
export function applyQuaternionToVector(q: Quaternion, v: Vector3): Vector3 {
  // This is a simplified placeholder. Actual implementation involves quaternion-vector multiplication.
  // For now, it just returns the vector as is.
  console.warn("applyQuaternionToVector is a placeholder and does not perform actual rotation.");
  return { ...v };
}

/**
 * Transforms a pose by another pose (e.g., child_pose = parent_pose * transform_from_parent_to_child).
 * Simplified example, a proper implementation would involve concatenating transformations.
 */
export function transformPose(parentPose: Pose, childPoseLocal: Pose): Pose {
  // This is a simplified placeholder. Actual implementation involves complex matrix/quaternion math.
  console.warn("transformPose is a placeholder and does not perform actual pose transformation.");
  // For now, just combines positions and assumes child orientation is relative to parent.
  return {
    position: addVectors(parentPose.position, childPoseLocal.position),
    orientation: childPoseLocal.orientation // Simplified
  };
}
