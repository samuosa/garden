// src/components/DeviceControl.js
import React from 'react';
import axios from 'axios';

const DeviceControl = ({token}) => {
  const handleDeviceAction = async (deviceType, deviceId, action) => {
    try {
      const endpoint = deviceType === 'pump' ? '/pump' : '/ventilator';
      await axios.post(`http://192.168.178.127:5000${endpoint}`, {
        [`${deviceType}_id`]: deviceId,
        action: action,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert(`${deviceType} ${deviceId} turned ${action}`);
    } catch (error) {
      console.error(error);
      alert('Error controlling device');
    }
  };

  return (
    <div className="my-4">
      <h2>Device Control</h2>
      <div className="row">
        {/* Pumps */}
        <div className="col-md-6">
          <h3>Pumps</h3>
          {[1, 2].map((id) => (
            <div key={id}>
              <h5>Pump {id}</h5>
              <button
                className="btn btn-success mr-2"
                onClick={() => handleDeviceAction('pump', id, 'on')}
              >
                Turn On
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleDeviceAction('pump', id, 'off')}
              >
                Turn Off
              </button>
            </div>
          ))}
        </div>
        {/* Ventilators */}
        <div className="col-md-6">
          <h3>Ventilators</h3>
          {[1, 2].map((id) => (
            <div key={id}>
              <h5>Ventilator {id}</h5>
              <button
                className="btn btn-success mr-2"
                onClick={() => handleDeviceAction('ventilator', id, 'on')}
              >
                Turn On
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleDeviceAction('ventilator', id, 'off')}
              >
                Turn Off
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DeviceControl;
