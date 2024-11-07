// src/components/FillLevel.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FillLevel = ({token}) => {
  const [fill, setFillLevel] = useState(null);

  const fetchFillLevel = async () => {
    try {
      const response = await axios.get('http://192.168.178.127:5000/read_sensors', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.data);
      setFillLevel(response.data.fill_level);
    } catch (error) {
      console.error(error);
      alert('Error fetching fill');
    }
  };

  useEffect(() => {
    fetchFillLevel();
    const interval = setInterval(fetchFillLevel, 60000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  },[]);

  return (
    <div className="my-4">
      <h2>Tank fill level</h2>
      {fill !== null ? (
        <h3>{fill}%</h3>
      ) : (
        <p>Loading Tank fill data...</p>
      )}
    </div>
  );
};

export default FillLevel;
