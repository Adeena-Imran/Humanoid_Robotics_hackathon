# Implementation Tasks: Module 1 - The Robotic Nervous System (ROS 2)

**Feature**: `001-the-robotic-nervous-system`
**Status**: To Do

This document lists the implementation tasks for creating the content of Module 1, derived from the `spec.md` and `plan.md`. Tasks are designed to be achievable by a motivated learner and map directly to the learning plan.

## Task Format

- **ID**: A unique identifier for the task (e.g., T1.1).
- **Section**: Maps to the corresponding section in `plan.md`.
- **Type**: `Conceptual` or `Hands-on`.
- **Description**: A clear, actionable description of the task.

---

### Section 1: Introduction to ROS 2 - The "What" and "Why"

| ID   | Section | Type        | Description                                                                                                     |
|------|---------|-------------|-----------------------------------------------------------------------------------------------------------------|
| T1.1 | 1       | Conceptual  | Write the introductory chapter explaining what a robotics middleware is and why it's crucial for complex robots like humanoids. |
| T1.2 | 1       | Conceptual  | Draft a brief history of ROS, highlighting the key reasons for the transition from ROS 1 to ROS 2 (e.g., DDS, real-time support). |
| T1.3 | 1       | Hands-on    | Create a tutorial on installing ROS 2 and verifying the installation using built-in demo nodes (`talker`/`listener`). |
| T1.4 | 1       | Conceptual  | Produce a table of essential ROS 2 command-line tools (`ros2 run`, `ros2 topic`, `ros2 node`, etc.) with brief descriptions. |

---

### Section 2: Core ROS 2 Communication Concepts

| ID   | Section | Type        | Description                                                                                                                              |
|------|---------|-------------|------------------------------------------------------------------------------------------------------------------------------------------|
| T2.1 | 2       | Conceptual  | Create a chapter defining a ROS 2 Node and its role as a fundamental process in a ROS 2 system. Include a simple diagram.              |
| T2.2 | 2       | Conceptual  | Write a detailed explanation of ROS 2 Topics, covering the publish-subscribe pattern. Use a humanoid's camera feed as a practical example. |
| T2.3 | 2       | Conceptual  | Write a detailed explanation of ROS 2 Services, covering the request/reply pattern. Use a "get_joint_angle" service as an example.        |
| T2.4 | 2       | Conceptual  | Write a detailed explanation of ROS 2 Actions, covering the long-running, feedback-driven pattern. Use a "walk_to_target" action as an example. |
| T2.5 | 2       | Conceptual  | Create a comparative table that clearly outlines the differences and ideal use cases for Topics, Services, and Actions.                     |
| T2.6 | 2       | Conceptual  | Draft a simplified guide to ROS 2 QoS settings, explaining the concepts of Reliability and Durability with practical recommendations.      |

---

### Section 3: Practical ROS 2 with `rclpy`

| ID   | Section | Type        | Description                                                                                                                             |
|------|---------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| T3.1 | 3       | Hands-on    | Develop a step-by-step tutorial for creating a new ROS 2 package and workspace.                                                         |
| T3.2 | 3       | Hands-on    | Write a Python script (`rclpy`) for a publisher node that sends out mock humanoid joint states (`sensor_msgs/msg/JointState`).            |
| T3.3 | 3       | Hands-on    | Write a corresponding subscriber node in Python (`rclpy`) that listens to the joint states and prints them to the console.                |
| T3.4 | 3       | Hands-on    | Implement a ROS 2 service server in Python that takes a joint name (string) and returns a mock angle (float).                             |
| T3.5 | 3       | Hands-on    | Write a service client node in Python that calls the service from T3.4 and prints the result.                                             |
| T3.6 | 3       | Hands-on    | Create a simple action server in Python that simulates a humanoid robot "waving" its arm, providing feedback on the progress of the wave. |
| T3.7 | 3       | Hands-on    | Write an action client in Python that sends a goal to the "wave" action server and logs the feedback and final result.                  |

---

### Section 4: Describing Robots with URDF

| ID   | Section | Type        | Description                                                                                                                         |
|------|---------|-------------|-------------------------------------------------------------------------------------------------------------------------------------|
| T4.1 | 4       | Conceptual  | Write an introduction to URDF, explaining its purpose and XML-based syntax.                                                         |
| T4.2 | 4       | Hands-on    | Create a simple URDF file for a two-link robotic arm, defining the `link` and `joint` elements with visual and collision properties. |
| T4.3 | 4       | Conceptual  | Explain the different joint types in URDF (`revolute`, `continuous`, `prismatic`, `fixed`) with diagrams showing their motion.     |
| T4.4 | 4       | Hands-on    | Guide the reader on how to visualize the created URDF file in RViz2, demonstrating the link between the XML code and the 3D model. |
| T4.5 | 4       | Conceptual  | Provide and dissect a simplified URDF for a full humanoid robot, focusing on the hierarchical structure of the links and joints.    |

---

### General Tasks & Exercises

| ID   | Section | Type        | Description                                                                                                        |
|------|---------|-------------|--------------------------------------------------------------------------------------------------------------------|
| T5.1 | All     | Conceptual  | Create a glossary of all key terms introduced in the module (e.g., Node, Topic, URDF, rclpy, QoS).                   |
| T5.2 | All     | Hands-on    | Develop a set of end-of-module exercises (Easy, Medium, Hard) that require the reader to combine concepts from all sections. |
| T5.3 | All     | Conceptual  | Write assessment rubrics and solutions for the exercises in T5.2.                                                  |