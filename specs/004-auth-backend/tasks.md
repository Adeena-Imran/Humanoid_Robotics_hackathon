# Implementation Tasks: Module 4 - Vision-Language-Action (VLA)

**Feature**: `004-vision-language-action`
**Status**: To Do

This document lists the implementation tasks for the capstone Module 4, derived from the `spec.md` and `plan.md`. These tasks are integration-heavy, designed to bring together all concepts from the previous modules into a single, intelligent system.

## Task Format

-   **ID**: A unique identifier for the task (e.g., T1.1).
-   **Section**: Maps to the corresponding section in `plan.md`.
-   **Type**: `Conceptual`, `Configuration`, or `Hands-on`.
-   **Description**: A clear, actionable description of the task.

---

### Section 1: The End-to-End VLA Pipeline

| ID   | Section | Type       | Description                                                                                                                             |
| :--- | :------ | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| T1.1 | 1       | Conceptual | Write the introductory chapter that frames Module 4 as the capstone, integrating Modules 1-3 into a cognitive robotics system.             |
| T1.2 | 1       | Conceptual | Create the master architectural diagram of the VLA pipeline, showing all ROS 2 nodes, topics, and actions from voice input to robot execution. |
| T1.3 | 1       | Config     | Create a new ROS 2 package (e.g., `vla_system`) that will contain all the new nodes for this module.                                        |

---

### Section 2: From Voice to Text

| ID   | Section | Type       | Description                                                                                                                             |
| :--- | :------ | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| T2.1 | 2       | Hands-on   | Write a Python script (`speech_to_text_node.py`) that uses a library (e.g., `whisper`) to capture audio from a microphone.               |
| T2.2 | 2       | Hands-on   | Implement the ROS 2 node logic in the script to transcribe the captured audio into a text string.                                         |
| T2.3 | 2       | Hands-on   | Publish the transcribed text string to a `std_msgs/msg/String` message on the `/user_command` ROS 2 topic.                                |
| T2.4 | 2       | Config     | Create a launch file to run the `speech_to_text_node` and provide instructions for testing it independently.                              |

---

### Section 3: The LLM as a Cognitive Planner

| ID   | Section | Type       | Description                                                                                                                             |
| :--- | :------ | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| T3.1 | 3       | Conceptual | Write a detailed chapter on prompt engineering for robotics, including how to define the robot's capabilities and desired output format.    |
| T3.2 | 3       | Hands-on   | Write the system prompt for the humanoid robot, defining its available actions (`navigate_to`, `find_object`, `pick_up`) in the prompt.   |
| T3.3 | 3       | Hands-on   | Create a ROS 2 node (`llm_planner_node.py`) that subscribes to the `/user_command` topic.                                                 |
| T3.4 | 3       | Hands-on   | In the planner node, implement the logic to call an LLM API (local or remote) with the combined system prompt and user command.            |
| T3.5 | 3       | Hands-on   | Implement parsing and validation for the returned JSON plan. Publish the validated plan to a `/task_plan` topic (custom message type).    |

---

### Section 4: The ROS 2 Orchestrator

| ID   | Section | Type       | Description                                                                                                                             |
| :--- | :------ | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| T4.1 | 4       | Hands-on   | Create the main orchestrator node (`orchestrator_node.py`) that subscribes to the `/task_plan` topic.                                      |
| T4.2 | 4       | Hands-on   | Implement the core logic to parse the plan's sequence of tasks.                                                                           |
| T4.3 | 4       | Hands-on   | For a `navigate_to` task, implement a ROS 2 action client that calls the Nav2 action server and waits for the result before proceeding.     |
| T4.4 | 4       | Hands-on   | For a `find_object` task, implement a ROS 2 service client that calls a perception service (which would use Isaac ROS) to get object coordinates. |
| T4.5 | 4       | Hands-on   | Implement state management and logging within the orchestrator to report the current status (e.g., "Executing step 1: navigate_to kitchen..."). |

---

### Section 5: Assembling and Running the Full System (Capstone Project)

| ID   | Section | Type    | Description                                                                                                                                 |
| :--- | :------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| T5.1 | 5       | Config  | Create the master ROS 2 launch file (`capstone.launch.py`) that brings up the entire system: Isaac Sim, all Module 3 nodes, and all Module 4 nodes. |
| T5.2 | 5       | Hands-on | Write a detailed, step-by-step tutorial for running the full capstone scenario from a fresh terminal.                                          |
| T5.3 | 5       | Hands-on | Create a debugging guide showing how to use `ros2 topic echo`, `ros2 action list`, and RViz2 to inspect each part of the VLA pipeline.           |
| T5.4 | 5       | Conceptual | Write a concluding chapter on the challenges of VLA systems, including safety, interpretability, and the importance of robust system integration. |
| T5.5 | 5       | Hands-on | **(Capstone Milestone 1)**: User speaks "go to the kitchen." Robot successfully navigates to the kitchen using Nav2.                           |
| T5.6 | 5       | Hands-on | **(Capstone Milestone 2)**: User speaks "find the red apple." Robot navigates and uses its perception system to locate and point towards the apple. |
| T5.7 | 5       | Hands-on | **(Capstone Milestone 3)**: User speaks "pick up the red apple." Robot performs all steps, including a simulated grasping action.              |