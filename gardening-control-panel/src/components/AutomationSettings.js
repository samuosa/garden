// src/components/AutomationSettings.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AutomationSettings = ({token}) => {
  const [automationEnabled, setAutomationEnabled] = useState(true);
  const [threshold, setThreshold] = useState(30);

  const fetchAutomationSettings = async () => {
    try {
      // Assuming you have an endpoint to get current settings
      // If not, initialize with default or previous state
    } catch (error) {
      console.error(error);
    }
  };

  const updateAutomationSettings = async () => {
    try {
      await axios.post('http://192.168.178.127:5000/automation', {
        enabled: automationEnabled,
        threshold: parseInt(threshold),
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert('Automation settings updated');
    } catch (error) {
      console.error(error);
      alert('Error updating automation settings');
    }
  };

  useEffect(() => {
    fetchAutomationSettings();
  }, []);

  return (
    <div className="my-4">
      <h2>Automation Settings</h2>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={automationEnabled}
            onChange={(e) => setAutomationEnabled(e.target.checked)}
          />{' '}
          Enable Automation
        </label>
      </div>
      <div className="form-group">
        <label>Soil Moisture Threshold (%)</label>
        <input
          type="number"
          className="form-control"
          value={threshold}
          onChange={(e) => setThreshold(e.target.value)}
        />
      </div>
      <button className="btn btn-primary" onClick={updateAutomationSettings}>
        Save Settings
      </button>
    </div>
  );
};

export default AutomationSettings;
