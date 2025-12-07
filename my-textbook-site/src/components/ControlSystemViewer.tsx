// my-textbook-site/src/components/ControlSystemViewer.tsx

import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

interface ControlSystemViewerProps {
  data: {
    labels: string[]; // e.g., time
    datasets: {
      label: string;
      data: number[];
      borderColor: string;
      fill?: boolean;
    }[];
  };
  title: string;
}

/**
 * ControlSystemViewer component displays control system responses using Chart.js.
 * It provides a customizable chart for visualizing time-series data related to control
 * simulations, such as position, velocity, error, or control output over time.
 * Props:
 *   data: Chart.js data object - Contains labels and datasets for plotting.
 *   title: string - The title for the control system viewer.
 */
const ControlSystemViewer: React.FC<ControlSystemViewerProps> = ({ data, title }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    // Performance Optimization Notes for Chart.js:
    // - Debounce/throttle updates if data changes rapidly.
    // - Limit the number of data points rendered for long time series.
    // - Use Chart.js plugins for specific performance needs.
    // - Consider WebGL-accelerated charting libraries for very large datasets.
    if (chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      chartInstance.current = new Chart(chartRef.current, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { title: { display: true, text: 'Time (s)' } },
            y: { title: { display: true, text: 'Value' } }
          }
        }
      });
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);

  return (
    <div style={{ border: '1px solid lightgray', padding: '10px', margin: '10px 0', borderRadius: '5px' }}>
      <h3>{title}</h3>
      <div style={{ height: '300px', width: '100%' }}>
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
};

export default ControlSystemViewer;
