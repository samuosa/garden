import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const ViewReadings = () => {
  const [readings, setReadings] = useState([]);
  
  useEffect(() => {
    // Fetch data from the endpoint
    fetch('http://192.168.178.130:5000/all_readings')
      .then(response => response.json())
      .then(data => setReadings(data))
      .catch(error => console.error('Error fetching readings:', error));
  }, []);
  
  // Convert timestamps to HH:MM format
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  // Prepare data for each chart
  const timestamps = readings.map(r => formatTimestamp(r.timestamp));
  const humidityData = readings.map(r => r.humidity);
  const pressureData = readings.map(r => r.pressure);
  const temperatureData = readings.map(r => r.temperature);
  
  const createChartData = (label, data, color) => ({
    labels: timestamps,
    datasets: [
      {
        label,
        data,
        borderColor: color,
        fill: false,
        tension: 0.1,
      },
    ],
  });

  return (
    <div className="container my-4">
      <h2 className="text-center mb-4">Environmental Readings</h2>
      
      <div className="row">
        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Humidity</h5>
              <div style={{ height: '300px' }}>
                <Line data={createChartData('Humidity (%)', humidityData, 'blue')} />
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Air Pressure</h5>
              <div style={{ height: '300px' }}>
                <Line data={createChartData('Air Pressure (hPa)', pressureData, 'green')} />
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Temperature</h5>
              <div style={{ height: '300px' }}>
                <Line data={createChartData('Temperature (°C)', temperatureData, 'red')} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewReadings;
