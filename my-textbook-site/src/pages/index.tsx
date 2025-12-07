import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import styles from "./index.module.css";

export default function Home(){
  return (
    <Layout
      title="Humanoid Robotics Textbook"
      description="An interactive, modern textbook on humanoid robotics with modules, demos, and practical examples."
    >
      <header className={styles.heroBanner}>
        <div className="container">
          <h1 className="hero__title">Physical AI and Humanoid Robotics Textbook</h1>
          <p className="hero__subtitle">
            Learn kinematics, perception, control systems, and actuators — with interactive demos.
          </p>

          <div className={styles.buttons}>
            <Link className="button button--primary button--lg" to="/docs/intro-humanoid-robotics">
              Start Learning
            </Link>
          </div>
        </div>
      </header>

      <main className="container margin-vert--lg">
        <h2 className="text--center">📘 Course Modules</h2>

        <div className={styles.modulesGrid}>

          {/* ------------------- MODULE 1 -------------------- */}
          <div className={styles.moduleCard}>
            <h3>Module 1: Introduction to Humanoid Robotics</h3>
            <p>Basics of humanoid robots, applications, and structure.</p>
            <Link to="/docs/intro-humanoid-robotics">Open Module →</Link>
          </div>

          {/* ------------------- MODULE 2 -------------------- */}
          <div className={styles.moduleCard}>
            <h3>Module 2: Kinematics & Motion</h3>
            <ul>
              <li><Link to="/docs/module2/forward-kinematics">Forward Kinematics</Link></li>
              <li><Link to="/docs/module2/inverse-kinematics">Inverse Kinematics</Link></li>
            </ul>
          </div>

          {/* ------------------- MODULE 3 -------------------- */}
          <div className={styles.moduleCard}>
            <h3>Module 3: Sensors & Perception</h3>
            <ul>
              <li><Link to="/docs/module3/sensor-types">Sensor Types</Link></li>
              <li><Link to="/docs/module3/basic-localization">Localization</Link></li>
            </ul>
          </div>

          {/* ------------------- MODULE 4 -------------------- */}
          <div className={styles.moduleCard}>
            <h3>Module 4: Actuators & Control</h3>
            <ul>
              <li><Link to="/docs/module4/actuator-types">Actuator Types</Link></li>
              <li><Link to="/docs/module4/pid-control">PID Control</Link></li>
            </ul>
          </div>

        </div>
      </main>
    </Layout>
  );
}

