# Data Model: Module 2 - Kinematics and Motion of Humanoid Robots

**Date**: 2025-12-07
**Feature**: [Kinematics and Motion of Humanoid Robots](specs/001-humanoid-kinematics/spec.md)

## Key Entities and Relationships

### 1. Humanoid Robot Model

*   **Description**: Represents the overall physical structure and kinematic properties of a humanoid robot.
*   **Fields**:
    *   `id`: Unique identifier for the robot model.
    *   `name`: Descriptive name (e.g., "NAO", "Atlas").
    *   `description`: General description of the robot.
    *   `base_link`: Reference to the root `Link` of the robot.
    *   `kinematic_chains`: List of associated `Kinematic Chain` entities.
*   **Relationships**: Has many `Links`, many `Joints`, many `Kinematic Chains`.

### 2. Link

*   **Description**: A rigid body segment of the robot's structure.
*   **Fields**:
    *   `id`: Unique identifier for the link.
    *   `name`: Name of the link (e.g., "torso", "upper_arm", "forearm").
    *   `geometry`: Shape and dimensions of the link.
    *   `mass_properties`: Mass, center of mass, inertia tensor.
    *   `parent_joint`: Reference to the `Joint` connecting it to its parent link.
    *   `child_joints`: List of `Joint` entities connecting to child links.
*   **Relationships**: Connected to other `Links` via `Joints`. Forms part of a `Kinematic Chain`.

### 3. Joint

*   **Description**: A connection between two `Links` that allows relative motion.
*   **Fields**:
    *   `id`: Unique identifier for the joint.
    *   `name`: Name of the joint (e.g., "shoulder_pitch", "elbow_yaw").
    *   `type`: Type of joint (e.g., "revolute", "prismatic").
    *   `axis`: Vector defining the axis of rotation/translation.
    *   `limits`: Minimum and maximum angular/linear displacement.
    *   `parent_link`: Reference to the `Link` on the parent side of the joint.
    *   `child_link`: Reference to the `Link` on the child side of the joint.
    *   `default_angle/position`: Default configuration.
*   **Relationships**: Connects two `Links`. Part of a `Kinematic Chain`.

### 4. Kinematic Chain

*   **Description**: A series of connected `Links` and `Joints` from a base to an `End-Effector`.
*   **Fields**:
    *   `id`: Unique identifier.
    *   `name`: Name (e.g., "right_arm", "left_leg").
    *   `base_link`: Reference to the starting `Link` of the chain.
    *   `end_effector`: Reference to the `End-Effector` of the chain.
    *   `links_sequence`: Ordered list of `Link` references in the chain.
    *   `joints_sequence`: Ordered list of `Joint` references in the chain.
*   **Relationships**: Composed of `Links` and `Joints`. Terminates at an `End-Effector`. Belongs to a `Humanoid Robot Model`.

### 5. End-Effector

*   **Description**: The operational part of the robot that interacts with the environment.
*   **Fields**:
    *   `id`: Unique identifier.
    *   `name`: Name (e.g., "right_hand", "left_foot").
    *   `attached_link`: Reference to the `Link` it is attached to.
    *   `local_transform`: Transform from `attached_link` frame to `End-Effector` frame.
*   **Relationships**: Attached to a `Link`. Part of a `Kinematic Chain`.

### 6. Coordinate Frame

*   **Description**: A reference system for defining positions and orientations in 3D space.
*   **Fields**:
    *   `id`: Unique identifier.
    *   `name`: Name (e.g., "world_frame", "base_frame", "joint_frame").
    *   `origin`: Position (x, y, z).
    *   `orientation`: Orientation (e.g., quaternion or rotation matrix).
    *   `parent_frame`: Reference to the `Coordinate Frame` it is defined relative to.
*   **Relationships**: Can be nested (parent-child relationship). Associated with `Links` and `Joints`.

### 7. Trajectory

*   **Description**: A time-parameterized path for a robot's motion.
*   **Fields**:
    *   `id`: Unique identifier.
    *   `name`: Descriptive name (e.g., "reach_target_A", "walk_forward").
    *   `type`: Type of trajectory (e.g., "joint_space", "task_space").
    *   `points`: Sequence of (time, pose/joint_angles) pairs.
    *   `duration`: Total time of the trajectory.
*   **Relationships**: Applies to a `Humanoid Robot Model` or specific `Kinematic Chains`.
