import React, { useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import LiveView from './LiveView';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const ViewReadings = ({ token }) => {
  const [readings, setReadings] = useState([]);
  const [wateringData, setWateringData] = useState([]);
  const [filter, setFilter] = useState('all');
  const [waterAmount, setWaterAmount] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [confirmation, setConfirmation] = useState('');
  const [schedules, setSchedules] = useState([]);
  const [newSchedule, setNewSchedule] = useState({ time: '', volume: '' });
  const [scheduleConfirmation, setScheduleConfirmation] = useState('');

  useEffect(() => {
    // Fetch data from the endpoint
    fetch('http://192.168.178.130:5000/all_readings')
      .then(response => response.json())
      .then(data => setReadings(data))
      .catch(error => console.error('Error fetching readings:', error));

    // Fetch watering data from the endpoint
    fetch('http://192.168.178.130:5000/watering')
      .then(response => response.json())
      .then(data => {
        setWateringData(data);
      })
      .catch(error => console.error('Error fetching watering data:', error));

    // Fetch schedules from the endpoint
    fetch('http://192.168.178.130:5000/schedules')
      .then(response => response.json())
      .then(data => setSchedules(data))
      .catch(error => console.error('Error fetching schedules:', error));
  }, []);

  // Filter data based on the selected filter
  const filterData = (data) => {
    const now = new Date();
    if (filter === 'last24h') {
      return data.filter(item => new Date(item.timestamp) >= new Date(now.getTime() - 24 * 60 * 60 * 1000));
    } else if (filter === 'lastWeek') {
      return data.filter(item => new Date(item.timestamp) >= new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000));
    } else if (filter === 'lastMonth') {
      return data.filter(item => new Date(item.timestamp) >= new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000));
    }
    return data;
  };

  // Convert timestamps based on the selected filter
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    if (filter === 'last24h') {
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    } else {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      return `${day}.${month}`;
    }
  };

  // Prepare data for each chart
  const filteredReadings = filterData(readings);
  const filteredWateringData = filterData(wateringData);

  const timestamps = filteredReadings.map(r => formatTimestamp(r.timestamp));
  const humidityData = filteredReadings.map(r => r.humidity);
  const pressureData = filteredReadings.map(r => r.pressure);
  const temperatureData = filteredReadings.map(r => r.temperature);

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

  // Prepare data for the watering bar chart
  const wateringDates = filteredWateringData.map(w => formatTimestamp(w.timestamp));
  const wateringAmounts = filteredWateringData.map(w => w.volume);

  const wateringChartData = {
    labels: wateringDates,
    datasets: [
      {
        label: 'Watering Amount (ml)',
        data: wateringAmounts,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Handle water pump request
  const handleWaterSubmit = async () => {
    setIsSending(true);
    setConfirmation('');
    try {
      const response = await fetch('http://192.168.178.130:5000/pump', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ml: parseInt(waterAmount) }),
      });

      if (response.ok) {
        setConfirmation('Watering request successfully sent!');
      } else {
        setConfirmation('Failed to send watering request.');
      }
    } catch (error) {
      setConfirmation('An error occurred while sending the request.');
    } finally {
      setIsSending(false);
      setWaterAmount('');
    }
  };

  // Handle new schedule submission
  const handleScheduleSubmit = async () => {
    setScheduleConfirmation('');
    try {
      const response = await fetch('http://192.168.178.130:5000/schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSchedule),
      });

      if (response.ok) {
        setScheduleConfirmation('Schedule successfully set!');
        setNewSchedule({ time: '', volume: '' });
        // Refresh schedules
        fetch('http://192.168.178.130:5000/schedules')
          .then(response => response.json())
          .then(data => setSchedules(data))
          .catch(error => console.error('Error fetching schedules:', error));
      } else {
        setScheduleConfirmation('Failed to set schedule.');
      }
    } catch (error) {
      setScheduleConfirmation('An error occurred while setting the schedule.');
    }
  };

  // Handle schedule deletion
  const handleScheduleDelete = async (time) => {
    try {
      const response = await fetch('http://192.168.178.130:5000/schedule', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ time }),
      });

      if (response.ok) {
        setScheduleConfirmation(`Schedule at ${time} successfully deleted!`);
        // Refresh schedules
        fetch('http://192.168.178.130:5000/schedules')
          .then(response => response.json())
          .then(data => setSchedules(data))
          .catch(error => console.error('Error fetching schedules:', error));
      } else {
        setScheduleConfirmation('Failed to delete schedule.');
      }
    } catch (error) {
      setScheduleConfirmation('An error occurred while deleting the schedule.');
    }
  };

  return (
    <div className="container my-4">
      <h2 className="text-center mb-4">Environmental Readings</h2>

      <div className="mb-4 text-center">
        <label htmlFor="filter" className="mr-2">Select Time Range: </label>
        <select id="filter" value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All Time</option>
          <option value="lastMonth">Last Month</option>
          <option value="lastWeek">Last Week</option>
          <option value="last24h">Last 24 Hours</option>
        </select>
      </div>

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

        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Live view</h5>
              <LiveView token={token} />
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Watering</h5>
              <div style={{ height: '300px' }}>
                <Bar data={wateringChartData} />
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card" style={{ height: '200px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Water Pump Control</h5>
              <div className="input-group mb-3">
                <input
                  type="number"
                  className="form-control"
                  placeholder="Enter amount to pump (ml)"
                  value={waterAmount}
                  onChange={(e) => setWaterAmount(e.target.value)}
                  disabled={isSending}
                />
                <div className="input-group-append">
                  <button
                    className="btn btn-primary"
                    type="button"
                    onClick={handleWaterSubmit}
                    disabled={isSending}
                  >
                    {isSending ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </div>
              {isSending && <div className="text-center my-2"><span className="spinner-border spinner-border-sm"></span></div>}
              {confirmation && <div className="text-center text-success mt-2">{confirmation}</div>}
            </div>
          </div>
        </div>

        <div className="col-md-12 mb-4">
          <div className="card" style={{ height: '400px' }}>
            <div className="card-body">
              <h5 className="card-title text-center">Manage Watering Schedules</h5>
              <div className="input-group mb-3">
                <input
                  type="time"
                  className="form-control"
                  value={newSchedule.time}
                  onChange={(e) => setNewSchedule({ ...newSchedule, time: e.target.value })}
                />
                <input
                  type="number"
                  className="form-control"
                  placeholder="Volume (ml)"
                  value={newSchedule.volume}
                  onChange={(e) => setNewSchedule({ ...newSchedule, volume: e.target.value })}
                />
                <div className="input-group-append">
                  <button
                    className="btn btn-primary"
                    type="button"
                    onClick={handleScheduleSubmit}
                  >
                    Set Schedule
                  </button>
                </div>
              </div>
              {scheduleConfirmation && <div className="text-center text-success mt-2">{scheduleConfirmation}</div>}

              <h6 className="mt-4">Current Schedules:</h6>
              <ul className="list-group">
                {schedules.map((schedule, index) => (
                  <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                    {`Time: ${schedule.time}, Volume: ${schedule.volume} ml`}
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleScheduleDelete(schedule.time)}
                    >
                      Delete
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewReadings;
