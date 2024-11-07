// src/components/TempHumidity.js
import React, { useState, useEffect } from "react";
import axios from "axios";

const TempHumidity = ({ token }) => {
  const [humidity, setHumidity] = useState(null);
  const [pressure, setPressure] = useState(null);
  const [temperature, setTemperature] = useState(null);

  const fetchSoilMoisture = async () => {
    try {
      const response = await axios.get("http://192.168.178.127:5000/air", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.data);
      setHumidity(response.data.humidity);
      setPressure(response.data.pressure);
      setTemperature(response.data.temperature);
    } catch (error) {
      console.error(error);
      alert("Error fetching soil moisture");
    }
  };

  useEffect(() => {
    fetchSoilMoisture();
    const interval = setInterval(fetchSoilMoisture, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  });

  return (
    <div className="container">
      {/* First Row */}
      <div className="row">
        <div className="col-md-4 my-4">
          <h2>Temperature</h2>
          {temperature !== null ? (
            <h3>{temperature}°</h3>
          ) : (
            <p>Loading Air data...</p>
          )}
        </div>
        <div className="col-md-4 my-4">
          <h2>Humidity</h2>
          {humidity !== null ? (
            <h3>{humidity}%</h3>
          ) : (
            <p>Loading Air data...</p>
          )}
        </div>
        <div className="col-md-4 my-4">
          <h2>Pressure</h2>
          {pressure !== null ? (
            <h3>{pressure} hPa</h3>
          ) : (
            <p>Loading Air data...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TempHumidity;
