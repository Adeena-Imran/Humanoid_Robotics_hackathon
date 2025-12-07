// my-textbook-site/src/components/ActuatorTypesDemo.tsx

import React, { useState } from 'react';
import { Actuator } from '../lib/control-model';
import { createPose, createVector3, createQuaternion } from '../lib/robot-model'; // Reusing from robot-model

// Dummy Actuator Data
const dummyActuators: Actuator[] = [
  {
    id: 'motor1',
    name: 'DC Motor',
    type: 'MOTOR_DC',
    specifications: { maxTorque: '10 Nm', maxSpeed: '5000 RPM', voltage: '24V' },
    mountPoint: createPose(createVector3(0.1, 0, 0), createQuaternion(0, 0, 0, 1)),
    controlledJointId: 'joint1' // Example
  },
  {
    id: 'hydraulic1',
    name: 'Hydraulic Actuator',
    type: 'HYDRAULIC',
    specifications: { maxForce: '500 N', stroke: '0.1m', pressure: '10 MPa' },
    mountPoint: createPose(createVector3(0.2, 0, 0), createQuaternion(0, 0, 0, 1)),
    controlledJointId: 'joint2' // Example
  },
  {
    id: 'sea1',
    name: 'Series Elastic Actuator (SEA)',
    type: 'SEA',
    specifications: { maxTorque: '20 Nm', seriesStiffness: '1000 Nm/rad' },
    mountPoint: createPose(createVector3(0.3, 0, 0), createQuaternion(0, 0, 0, 1)),
    controlledJointId: 'joint3' // Example
  }
];

interface ActuatorTypesDemoProps {}

/**
 * ActuatorTypesDemo component provides an interactive way to explore different types of actuators
 * used in humanoid robots. Users can select an actuator to view its specifications and properties.
 * This component visualizes various actuator characteristics.
 */
const ActuatorTypesDemo: React.FC<ActuatorTypesDemoProps> = () => {
  const [selectedActuatorId, setSelectedActuatorId] = useState<string | null>(null);
  const selectedActuator = dummyActuators.find(a => a.id === selectedActuatorId);

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Explore Humanoid Robot Actuator Types</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px' }}>
        {dummyActuators.map(actuator => (
          <button
            key={actuator.id}
            onClick={() => setSelectedActuatorId(actuator.id)}
            style={{
              padding: '10px 15px',
              backgroundColor: selectedActuatorId === actuator.id ? '#007bff' : '#f0f0f0',
              color: selectedActuatorId === actuator.id ? 'white' : 'black',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}
          >
            {actuator.name} ({actuator.type})
          </button>
        ))}
      </div>

      {selectedActuator ? (
        <div>
          <h3>{selectedActuator.name} ({selectedActuator.type})</h3>
          <p><strong>Specifications:</strong> {JSON.stringify(selectedActuator.specifications)}</p>
          <p><strong>Mount Point:</strong> X:{selectedActuator.mountPoint.position.x.toFixed(2)}, Y:{selectedActuator.mountPoint.position.y.toFixed(2)}, Z:{selectedActuator.mountPoint.position.z.toFixed(2)}</p>
          <p><strong>Controls Joint:</strong> {selectedActuator.controlledJointId}</p>
          {/* Further details on advantages/limitations could go here */}
          <p><em>(Detailed advantages and limitations for {selectedActuator.name} would be presented here based on content)</em></p>
        </div>
      ) : (
        <p>Select an actuator to view its details.</p>
      )}
    </div>
  );
};

export default ActuatorTypesDemo;
