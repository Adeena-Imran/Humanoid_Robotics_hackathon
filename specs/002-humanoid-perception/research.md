# Research Findings: Module 3 - Sensors and Perception in Humanoid Robots

**Date**: 2025-12-07
**Feature**: [Sensors and Perception in Humanoid Robots](specs/002-humanoid-perception/spec.md)

## Resolution of "NEEDS CLARIFICATION" from Technical Context

### Specific Sensor Data Visualization Libraries

*   **Decision**:
    *   For 3D point clouds and general 3D sensor visualizations: `three.js` with custom shaders or libraries built on `three.js` (e.g., `react-three-fiber` for React integration).
    *   For 2D image data processing and visualization: Standard HTML `Canvas` API, potentially integrating with `OpenCV.js` for more advanced image processing within the browser.
    *   For IMU (Inertial Measurement Unit) data plots (e.g., acceleration, angular velocity over time): Charting libraries such as `Chart.js` or `Recharts`.
*   **Rationale**: These libraries offer a good balance of capability, community support, and web-compatibility. `three.js` is a standard for browser 3D, Canvas for 2D, and charting libraries for data visualization. `OpenCV.js` provides powerful image processing capabilities directly in JavaScript.
*   **Alternatives considered**: Babylon.js (similar to three.js, but three.js has slightly larger ecosystem for general 3D), custom WebGL (rejected for higher development effort).

### Handling Large Datasets and Saving User-Generated Data

*   **Decision**: For the initial implementation, interactive elements will focus on small, embedded datasets processed entirely client-side. No user progress or user-generated content (like custom maps) will be persisted dynamically.
*   **Rationale**: Simplifies the initial development and deployment, leveraging the static nature of Docusaurus. Reduces server-side infrastructure needs.
*   **Alternatives considered**:
    *   For processing large client-side datasets: Web Workers (to avoid blocking the main thread) or WebAssembly (for performance-critical parts).
    *   For saving user data or processing large datasets server-side: Implement a dedicated backend (e.g., FastAPI with Python, Node.js with Express) with a database (e.g., MongoDB for flexibility, PostgreSQL for structured data) and cloud storage (e.g., AWS S3, Google Cloud Storage) for very large sensor datasets. (Rejected for initial scope due to added complexity).

### Performance Metrics for Complex Perception Algorithms

*   **Decision**:
    *   Processing time for single-frame perception updates (e.g., object detection on a new image/point cloud): Target <100ms.
    *   Interaction latency (time from user input to visual feedback in simulations): Target <50ms.
    *   Memory usage: Keep browser tab memory footprint below 500MB for typical interactive demos involving 3D data.
    *   Frame Rate for 3D visualizations: Target 30-60 FPS on modern browsers.
*   **Rationale**: These metrics aim to ensure a responsive and smooth user experience without requiring high-end client hardware, balancing complexity with accessibility.
*   **Alternatives considered**: Stricter performance goals (rejected as potentially over-engineering for educational demos), looser goals (rejected as would lead to poor user experience).

### Expected Number of Concurrent Students and Peak Usage

*   **Decision**: For the initial phase, all interactive elements are designed to run client-side within the user's browser. The Docusaurus site itself will be hosted on a standard static hosting platform (e.g., GitHub Pages, Netlify, Vercel). These platforms are inherently scalable for serving static content to a large number of concurrent users. No specific server-side concurrency or peak usage metrics are defined for the interactive elements themselves, as they do not rely on a dedicated backend server for their execution.
*   **Rationale**: This approach minimizes infrastructure complexity and operational costs for the initial module rollout. Scalability is handled by the static hosting provider.
*   **Alternatives considered**: Hosting dynamic elements on a dedicated server (rejected for initial scope due to increased infrastructure and management overhead), using serverless functions for interactive elements (rejected for initial scope due to potential latency and cost for continuous interaction).