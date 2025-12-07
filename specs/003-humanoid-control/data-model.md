# Data Model: Module 4 - Actuation and Control Systems in Humanoid Robots

**Date**: 2025-12-07
**Feature**: [Actuation and Control Systems in Humanoid Robots](specs/003-humanoid-control/spec.md)

## Key Entities and Relationships

### 1. Actuator

*   **Description**: A component that converts energy into mechanical motion.
*   **Fields**:
    *   `id`: Unique identifier for the actuator.
    *   `name`: Descriptive name (e.g., "Right Arm Motor", "Torso Hydraulic").
    *   `type`: Type of actuator (e.g., "MOTOR_DC", "MOTOR_BLDC", "HYDRAULIC", "PNEUMATIC", "SEA").
    *   `specifications`: Object containing actuator-specific parameters (e.g., `maxTorque`, `maxSpeed`, `powerRating`, `gearRatio`).
    *   `mountPoint`: Pose describing its location and orientation on the robot.
    *   `controlledJointId`: Reference to the `Joint` (from Module 2) this actuator controls.
*   **Relationships**: Controls a `Joint`. Part of a `Humanoid Robot Model`.

### 2. Controller

*   **Description**: A system that manages and regulates the behavior of other devices or systems, aiming to achieve a desired output.
*   **Fields**:
    *   `id`: Unique identifier for the controller.
    *   `name`: Name of the controller (e.g., "Joint Position PID", "Torque Inverse Dynamics").
    *   `type`: Category of controller (e.g., "PID", "STATE_SPACE", "INVERSE_DYNAMICS").
    *   `targetSystemId`: Reference to the `Joint` or `Kinematic Chain` (from Module 2) it targets.
    *   `parameters`: Configuration parameters for the controller (e.g., `kp`, `ki`, `kd` for PID).
*   **Relationships**: Controls an `Actuator` through a `Control Loop`. Can use `Sensor Data` (from Module 3) as feedback.

### 3. Control Loop

*   **Description**: The feedback mechanism used to maintain a desired system state by comparing measured output to a setpoint and adjusting inputs.
*   **Fields**:
    *   `id`: Unique identifier for the control loop.
    *   `type`: Type of control loop (e.g., "POSITION_CONTROL", "VELOCITY_CONTROL", "FORCE_CONTROL").
    *   `setpoint`: The desired value for the controlled variable.
    *   `feedbackSensorId`: Reference to the `Sensor` (from Module 3) providing feedback.
    *   `actuatorId`: Reference to the `Actuator` whose input is adjusted.
    *   `controllerId`: Reference to the `Controller` implementing the control logic.
*   **Relationships**: Connects `Sensor`, `Controller`, and `Actuator`.

### 4. Trajectory

*   **Description**: A planned path of motion for a robot or its components, which a control system attempts to follow. (Reused and extended from Module 2).
*   **Fields**:
    *   `id`: Unique identifier.
    *   `name`: Descriptive name (e.g., "joint_space_trajectory_walk", "task_space_grasp").
    *   `type`: Type of trajectory (e.g., "JOINT_SPACE", "TASK_SPACE").
    *   `points`: Sequence of (time, pose/joint_angles) pairs, with interpolated values between points.
    *   `duration`: Total time of the trajectory.
    *   `velocityLimits`: Maximum allowed joint velocities or end-effector speeds.
    *   `accelerationLimits`: Maximum allowed joint accelerations or end-effector accelerations.
*   **Relationships**: Generated for a `Humanoid Robot Model` or specific `Kinematic Chains`. Executed by a `Control Loop`.
