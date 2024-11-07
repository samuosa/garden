// src/App.js
import React from "react";
import DeviceControl from "./components/DeviceControl";
import SoilMoisture from "./components/SoilMoisture";
import AutomationSettings from "./components/AutomationSettings";
import "bootstrap/dist/css/bootstrap.min.css";
import TempHumidity from "./components/TempHumidity";
import Login from "./components/Login";
import FillLevel from "./components/FillLevel";
import LiveView from "./components/LiveView";
import ViewReadings from "./components/ViewReadings";

function App() {
  const [token, setToken] = React.useState(null);

  return (
    <div className="container">
      <ViewReadings />
      {/*
      {token ? (
        <>
          <h1 className="my-4">Gardening Control Panel</h1>
          <FillLevel token={token}/>
          <LiveView token={token}/>
          <SoilMoisture token={token}/>
          <TempHumidity token={token}/> 
          <DeviceControl token={token}/>
          <AutomationSettings token={token}/>
        </>
      ) : (
        <>
          <Login setToken={setToken}/>
        </>
      )}
        */}
    </div>
  );
}

export default App;
