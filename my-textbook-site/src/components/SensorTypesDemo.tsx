// my-textbook-site/src/components/SensorTypesDemo.tsx

import React, { useState } from 'react';
import { Sensor } from '../lib/perception-model';

// Dummy Sensor Data
const dummySensors: Sensor[] = [
  {
    id: 'cam1',
    name: 'Front Camera',
    type: 'CAMERA',
    specifications: { resolution: '1280x720', fov: '90deg' },
    mountPoint: {
      position: { x: 0.1, y: 0, z: 0.8 },
      orientation: { x: 0, y: 0, z: 0, w: 1 }
    }
  },
  {
    id: 'imu1',
    name: 'Body IMU',
    type: 'IMU',
    specifications: { frequency: '100Hz', accuracy: '0.1deg/s' },
    mountPoint: {
      position: { x: 0, y: 0, z: 0.5 },
      orientation: { x: 0, y: 0, z: 0, w: 1 }
    }
  },
  {
    id: 'lidar1',
    name: 'Head LiDAR',
    type: 'LIDAR',
    specifications: { range: '0.1-10m', horizontalFOV: '360deg' },
    mountPoint: {
      position: { x: 0, y: 0, z: 0.9 },
      orientation: { x: 0, y: 0, z: 0, w: 1 }
    }
  },
  {
    id: 'fts1',
    name: 'Right Foot F/T Sensor',
    type: 'FORCE_TORQUE',
    specifications: { axes: '6', capacity: '100N' },
    mountPoint: {
      position: { x: 0, y: -0.2, z: 0 },
      orientation: { x: 0, y: 0, z: 0, w: 1 }
    }
  }
];

interface SensorTypesDemoProps { }

const SensorTypesDemo: React.FC<SensorTypesDemoProps> = () => {
  const [selectedSensorId, setSelectedSensorId] = useState<string | null>(null);
  const selectedSensor = dummySensors.find(s => s.id === selectedSensorId);

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Explore Humanoid Robot Sensor Types</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px' }}>
        {dummySensors.map(sensor => (
          <button
            key={sensor.id}
            onClick={() => setSelectedSensorId(sensor.id)}
            style={{
              padding: '10px 15px',
              backgroundColor: selectedSensorId === sensor.id ? '#007bff' : '#f0f0f0',
              color: selectedSensorId === sensor.id ? 'white' : 'black',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}
          >
            {sensor.name} ({sensor.type})
          </button>
        ))}
      </div>

      {selectedSensor ? (
        <div>
          <h3>{selectedSensor.name} ({selectedSensor.type})</h3>
          <p><strong>Specifications:</strong> {JSON.stringify(selectedSensor.specifications)}</p>
          <p>
            <strong>Mount Point:</strong> 
            X:{selectedSensor.mountPoint.position.x.toFixed(2)}, 
            Y:{selectedSensor.mountPoint.position.y.toFixed(2)}, 
            Z:{selectedSensor.mountPoint.position.z.toFixed(2)}
          </p>
          <p><em>(Detailed advantages and limitations for {selectedSensor.name} would be presented here.)</em></p>
        </div>
      ) : (
        <p>Select a sensor to view its details.</p>
      )}
    </div>
  );
};

export default SensorTypesDemo;
