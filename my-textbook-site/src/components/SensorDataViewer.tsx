// my-textbook-site/src/components/SensorDataViewer.tsx

import React, { useEffect, useRef } from 'react';
import { SensorData } from '../lib/perception-model';
import Chart from 'chart.js/auto'; // Import Chart.js

interface SensorDataViewerProps {
  sensorData: SensorData[];
  title: string;
}

/**
 * SensorDataViewer component displays sensor data, primarily visualizing IMU data using Chart.js.
 * It also provides a fallback to display raw data for other sensor types.
 * Props:
 *   sensorData: SensorData[] - An array of sensor data objects to display.
 *   title: string - The title for the sensor data viewer.
 */
const SensorDataViewer: React.FC<SensorDataViewerProps> = ({ sensorData, title }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    // Performance Optimization Notes for Chart.js:
    // - Debounce/throttle updates if sensorData changes rapidly.
    // - Limit the number of data points rendered for long time series.
    // - Use Chart.js plugins for specific performance needs.
    // - Consider WebGL-accelerated charting libraries for very large datasets.
    if (chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy(); // Destroy old chart instance
      }

      const imuData = sensorData.filter(d => d.type === 'IMU_READING' && typeof d.value === 'object');
      if (imuData.length > 0) {
        const labels = imuData.map(d => new Date(d.timestamp).toLocaleTimeString());
        const accelerationX = imuData.map(d => d.value.acceleration?.x || 0);
        const accelerationY = imuData.map(d => d.value.acceleration?.y || 0);
        const accelerationZ = imuData.map(d => d.value.acceleration?.z || 0);

        chartInstance.current = new Chart(chartRef.current, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              { label: 'Accel X', data: accelerationX, borderColor: 'red', fill: false },
              { label: 'Accel Y', data: accelerationY, borderColor: 'green', fill: false },
              { label: 'Accel Z', data: accelerationZ, borderColor: 'blue', fill: false },
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { beginAtZero: true },
              y: { beginAtZero: true }
            }
          }
        });
      } else {
        // Handle non-chartable data types here (e.g., images, point clouds)
        // For now, just display raw data below the canvas
      }
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [sensorData]);

  // Render raw data for non-chartable types or as fallback
  const rawDataDisplay = sensorData.map((data, index) => (
    <div key={data.id || index} style={{ marginBottom: '5px', fontSize: '0.8em' }}>
      <strong>{data.type} ({new Date(data.timestamp).toLocaleTimeString()}):</strong>{' '}
      {typeof data.value === 'object' ? JSON.stringify(data.value, null, 2) : String(data.value)}
    </div>
  ));

  return (
    <div style={{ border: '1px solid lightgray', padding: '10px', margin: '10px 0', borderRadius: '5px' }}>
      <h3>{title}</h3>
      {sensorData.length === 0 ? (
        <p>No sensor data available.</p>
      ) : (
        <>
          {/* Canvas for Chart.js - primarily for IMU data */}
          <div style={{ height: '300px', width: '100%', marginBottom: '10px' }}>
            <canvas ref={chartRef}></canvas>
          </div>
          {/* Display other data types or raw data */}
          {rawDataDisplay}
        </>
      )}
    </div>
  );
};

export default SensorDataViewer;
