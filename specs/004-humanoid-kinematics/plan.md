# Learning Plan: Module 4 - Vision-Language-Action (VLA)

**Feature**: `004-vision-language-action`
**Status**: Draft

This plan outlines the learning progression for the capstone module, which integrates all co
ncepts from Modules 1-3 to build an end-to-end autonomous system capable of understanding na
tural language commands and executing them in a simulated world.

## 1. Architectural Vision

This module is the culmination of the entire book. We will assemble the final "cognitive lay
er" of our humanoid robot, enabling it to process spoken commands, formulate a plan, and exe
cute it using the ROS 2, simulation, and perception systems we've already built. The archite
ctural focus is on system integration and orchestration, demonstrating how a Large Language 
Model (LLM) can act as a "brain," connecting language to perception and action. This plan br
idges the high-level goals of the capstone project in `spec.md` to the concrete implementati
on steps in `tasks.md`.

## 2. Progressive Learning Sections: Building the Capstone

The module will be structured as a step-by-step guide to building and running the final caps
tone project.

### Section 1: The End-to-End VLA Pipeline

-   **Objective**: Present a high-level overview of the complete Vision-Language-Action arch
itecture.
-   **Key Topics**:
    -   **The Goal**: From "Bring me the red apple" to robotic action.
    -   **The Pipeline**: A breakdown of the data flow:
        1.  **Voice Input**: Capturing audio.
        2.  **Speech-to-Text**: Converting audio to a text prompt.
        3.  **LLM Planning**: Sending the prompt to an LLM to generate a structured plan.   
        4.  **ROS 2 Orchestration**: Parsing the plan and executing ROS 2 actions/services. 
        5.  **Perception & Action**: Using the systems from Module 3 (Nav2, Isaac ROS) to pe
rform the tasks.
-   **Diagrams**: A detailed, top-to-bottom architectural diagram illustrating every compone
nt and the ROS 2 topics/actions connecting them. This is the master blueprint for the module
.

### Section 2: From Voice to Text

-   **Objective**: Implement the first stage of the pipeline: converting a spoken command in
to a usable text string.
-   **Key Topics**:
    -   Setting up a Python environment to capture microphone input.
    -   Using an open-source speech-to-text system (e.g., a local Whisper model) to transcri
be the audio.
    -   Creating a simple ROS 2 node that captures audio, transcribes it, and publishes the 
resulting text string to a `/user_command` topic.

### Section 3: The LLM as a Cognitive Planner

-   **Objective**: Teach the reader how to prompt an LLM to think like a robot and generate 
structured, machine-readable plans.
-   **Key Topics**:
    -   **Prompt Engineering for Robotics**: How to write a "system prompt" that defines the
 robot's capabilities (its available ROS 2 actions/services), its current state, and the des
ired output format (e.g., JSON).
    -   **Grounding the LLM**: Providing the LLM with a "world model" or context so its plan
s are relevant to the robot's environment and abilities.
    -   **Creating the Planner Node**: A ROS 2 node that subscribes to the `/user_command` t
opic, sends the text to an LLM API, and receives the structured plan.
-   **Example**: Show a full prompt and the corresponding structured JSON output for a comma
nd like "Get the soda can."
    ```json
    {
      "plan": [
        {"action": "navigate_to", "parameters": {"destination": "kitchen"}},
        {"action": "find_object", "parameters": {"object_name": "soda_can"}},
        {"action": "pick_up", "parameters": {"object_id": "result_of_step_2"}}
      ]
    }
    ```

### Section 4: The ROS 2 Orchestrator

-   **Objective**: Create the central node that translates the LLM's plan into actual robot 
behavior.
-   **Key Topics**:
    -   **The Orchestrator Node**: A Python-based ROS 2 node that subscribes to the LLM's pl
an topic.
    -   **Parsing and Execution Loop**: The node will parse the JSON plan and execute each s
tep sequentially.
    -   **Calling ROS 2 Actions**: The orchestrator will act as an action client, for exampl
e, to the Nav2 action server to execute `navigate_to` goals.
    -   **State Management**: The orchestrator must wait for one action to complete successf
ully before starting the next.
-   **Integration**: This section explicitly connects to the Nav2 and Isaac ROS perception p
ipelines built in Module 3.

### Section 5: Assembling and Running the Full System

-   **Objective**: Guide the reader through launching and testing the complete end-to-end sy
stem.
-   **Key Topics**:
    -   **The Master Launch File**: Creating a top-level ROS 2 launch file that starts:     
        -   Isaac Sim with the humanoid and environment.
        -   All required Isaac ROS perception and SLAM nodes (from Module 3).
        -   The Nav2 stack (from Module 3).
        -   The new VLA nodes: Speech-to-Text, LLM Planner, and Orchestrator.
    -   **Running a Full Scenario**: A step-by-step tutorial of the capstone project:       
        1.  Launch the system.
        2.  Speak the command.
        3.  Observe the robot performing the navigation and perception tasks.
    -   **Debugging and Visualization**: Using tools like RViz2 and `ros2 topic echo` to ins
pect each stage of the pipeline.

## 3. Risk Analysis

-   **Risk**: Access to powerful LLMs can be rate-limited or require payment.
    -   **Mitigation**: Base the examples on a locally runnable open-source model (e.g., a q
uantized Llama or Mistral model) to remove external dependencies. Provide clear instructions
 on setting up the local LLM server.
-   **Risk**: The complexity of the fully integrated system is high, making debugging diffic
ult.
    -   **Mitigation**: Structure each section so it can be tested independently. For exampl
e, allow the user to send a text command directly to the LLM planner, bypassing the voice in
put, to test that stage in isolation. Emphasize logging and clear status messages from the O
rchestrator node.

## 4. Definition of Done

The plan is considered complete when:
-   All sections align with the capstone project goals in `spec.md`.
-   The plan provides a clear, step-by-step path for assembling the final system.
-   The integration points between all four modules are explicitly defined.
-   The plan has been reviewed and approved.