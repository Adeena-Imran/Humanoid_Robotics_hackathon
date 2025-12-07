// my-textbook-site/src/lib/sensor-utils.ts

import { Vector3 } from './robot-model'; // Reusing Vector3 from robot-model
import { SensorData } from './perception-model';

/**
 * Generates Gaussian noise for a given value using the Box-Muller transform.
 * @param value The original value.
 * @param stdDev The standard deviation of the noise.
 * @returns Value with added Gaussian noise.
 */
export function addGaussianNoise(value: number, stdDev: number): number {
  if (stdDev === 0) return value;
  let u = 0, v = 0;
  while (u === 0) u = Math.random(); // Converting [0,1) to (0,1)
  while (v === 0) v = Math.random();
  const num = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  return value + num * stdDev;
}

/**
 * Simulates noise for a 3D vector.
 * @param vector The original 3D vector.
 * @param stdDev The standard deviation of the noise to apply to each component.
 * @returns A new Vector3 with added Gaussian noise.
 */
export function addVectorNoise(vector: Vector3, stdDev: number): Vector3 {
  return {
    x: addGaussianNoise(vector.x, stdDev),
    y: addGaussianNoise(vector.y, stdDev),
    z: addGaussianNoise(vector.z, stdDev),
  };
}

/**
 * Basic low-pass filter for scalar data.
 * Filters out high-frequency noise from a signal.
 * @param currentValue The current raw sensor reading.
 * @param previousFilteredValue The previously computed filtered value.
 * @param alpha The smoothing factor (0 to 1). A higher alpha means less smoothing and closer to current value.
 * @returns The new filtered value.
 */
export function lowPassFilter(currentValue: number, previousFilteredValue: number, alpha: number): number {
  return alpha * currentValue + (1 - alpha) * previousFilteredValue;
}

/**
 * Simulates a simple IMU reading with some noise.
 * @param trueAcceleration The actual (ground truth) acceleration vector.
 * @param trueAngularVelocity The actual (ground truth) angular velocity vector.
 * @param accelNoiseStdDev Standard deviation for acceleration noise.
 * @param gyroNoiseStdDev Standard deviation for gyroscope noise.
 * @returns Simulated IMU SensorData object.
 */
export function simulateIMUData(
  trueAcceleration: Vector3,
  trueAngularVelocity: Vector3,
  accelNoiseStdDev: number = 0.05,
  gyroNoiseStdDev: number = 0.01
): SensorData {
  return {
    id: `imu_data_${Date.now()}`,
    timestamp: Date.now(),
    type: 'IMU_READING',
    value: {
      acceleration: addVectorNoise(trueAcceleration, accelNoiseStdDev),
      angularVelocity: addVectorNoise(trueAngularVelocity, gyroNoiseStdDev),
      orientation: { x: 0, y: 0, z: 0, w: 1 } // Placeholder for orientation
    },
    sourceSensorId: 'simulated_imu_sensor'
  };
}

/**
 * Creates a dummy camera image SensorData.
 * @param width Image width.
 * @param height Image height.
 * @returns Simulated IMAGE SensorData.
 */
export function simulateCameraData(width: number, height: number): SensorData {
  // In a real scenario, this would generate an actual image or base64 string
  return {
    id: `camera_data_${Date.now()}`,
    timestamp: Date.now(),
    type: 'IMAGE',
    value: `data:image/svg+xml;base64,PHN2ZyB3aWR0aD0i${width}IiBoZWlnaHQ9I${height}IiB2aWV3Qm94PSIwIDAg${width} ${height}IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiNjY2MiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzMzMyI+Q2FtZXJhIEZlZWQ8L3RleHQ+PC9zdmc+`,
    sourceSensorId: 'simulated_camera_sensor'
  };
}

/**
 * Creates a dummy LiDAR point cloud SensorData.
 * @param numPoints Number of points in the cloud.
 * @param rangeMax Maximum range of the LiDAR.
 * @returns Simulated POINT_CLOUD SensorData.
 */
export function simulateLiDARData(numPoints: number, rangeMax: number): SensorData {
  const points: Vector3[] = [];
  for (let i = 0; i < numPoints; i++) {
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * rangeMax;
    points.push({
      x: distance * Math.cos(angle),
      y: distance * Math.sin(angle),
      z: (Math.random() - 0.5) * 0.5 // Small variation in Z
    });
  }
  return {
    id: `lidar_data_${Date.now()}`,
    timestamp: Date.now(),
    type: 'POINT_CLOUD',
    value: points,
    sourceSensorId: 'simulated_lidar_sensor'
  };
}
