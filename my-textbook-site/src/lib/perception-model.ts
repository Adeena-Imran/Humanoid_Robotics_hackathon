// my-textbook-site/src/lib/perception-model.ts

import { Pose, Vector3 } from './robot-model'; // Reusing from robot-model

/**
 * Represents a sensor device.
 */
export interface Sensor {
  id: string;
  name: string;
  type: 'CAMERA' | 'IMU' | 'LIDAR' | 'FORCE_TORQUE' | 'TACTILE';
  specifications: { [key: string]: any }; // Sensor-specific properties
  mountPoint: Pose; // Location and orientation on the robot
}

/**
 * Represents raw or processed information acquired from sensors.
 */
export interface SensorData {
  id: string;
  timestamp: number; // Unix timestamp
  type: 'IMAGE' | 'POINT_CLOUD' | 'IMU_READING' | 'FORCE_READING';
  value: any; // Data content (e.g., base64 string, array of numbers/objects)
  sourceSensorId: string; // Reference to the Sensor that generated this data
}

/**
 * Represents a computational method used to extract meaningful information from Sensor Data.
 */
export interface PerceptionAlgorithm {
  id: string;
  name: string;
  type: 'LOCALIZATION' | 'MAPPING' | 'OBJECT_RECOGNITION' | 'HUMAN_DETECTION';
  inputDataTypes: SensorData['type'][];
  outputDataTypes: ('POSE' | 'ENVIRONMENTAL_MAP' | 'FEATURE' | 'BOUNDING_BOX')[];
  parameters: { [key: string]: any }; // Algorithm-specific configuration
}

/**
 * Represents a distinct and identifiable characteristic extracted from sensor data.
 */
export interface Feature {
  id: string;
  type: 'CORNER' | 'EDGE' | 'POINT_CLUSTER' | 'LANDMARK' | 'OBJECT';
  location: Vector3; // Spatial coordinates of the feature
  descriptor: number[]; // Numerical signature (e.g., SIFT, SURF, ORB descriptor)
  sourceDataId: string; // Reference to the Sensor Data from which it was extracted
}

/**
 * A representation of the robot's surroundings, constructed from sensor data.
 */
export interface EnvironmentalMap {
  id: string;
  type: 'OCCUPANCY_GRID' | 'FEATURE_MAP' | 'POINT_CLOUD_MAP';
  resolution: number; // Spatial resolution (e.g., meters per cell)
  data: any; // Actual map content (e.g., 2D/3D grid of probabilities, list of Features)
  creationTimestamp: number;
}
