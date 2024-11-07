// src/components/SoilMoisture.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SoilMoisture = ({token}) => {
  const [moisture, setMoisture] = useState(null);

  const fetchSoilMoisture = async () => {
    try {
      const response = await axios.get('http://192.168.178.127:5000/soil_moisture', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMoisture(response.data.soil_moisture);
    } catch (error) {
      console.error(error);
      alert('Error fetching soil moisture');
    }
  };

  useEffect(() => {
    fetchSoilMoisture();
    const interval = setInterval(fetchSoilMoisture, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  });

  return (
    <div className="my-4">
      <h2>Soil Moisture</h2>
      {moisture !== null ? (
        <h3>{moisture}%</h3>
      ) : (
        <p>Loading soil moisture data...</p>
      )}
    </div>
  );
};

export default SoilMoisture;
