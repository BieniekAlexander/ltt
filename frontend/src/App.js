// imports
import React, { useState } from 'react';

import { fetchWeather } from './api/fetchWeather';
import './App.css';
import Popover from 'react-bootstrap/Popover';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Button from 'react-bootstrap/Button';

const App = () => {
  const [query, setQuery] = useState('');
  const [weather, setWeather] = useState({});

const search = async (e) => {
  if (e.key === 'Enter') {
    const data = await fetchWeather(query)

    setWeather(data);
    setQuery('');
  }
}

const popover = (
  <Popover id="popover-basic">
    <Popover.Header as="h3">Popover right</Popover.Header>
    <Popover.Body>
      And here's some <strong>amazing</strong> content. It's very engaging.
      right?
    </Popover.Body>
  </Popover>
);

const Example = () => (
  <div>
    <span>Click </span>
    <OverlayTrigger trigger="click" placement="right" overlay={popover}>
      <span>me </span>
      {/* variant="success" */}
    </OverlayTrigger>
    <span>to see</span>
  </div>
);




  return (
    <div className="main-container">
      <Example />
      
      <input type="text" className="search" placeholder="Search..." value={query} onChange={(e) => setQuery(e.target.value)} onKeyPress={search}/>
      {weather.main && (
        <div className="city">
          <h2 className="city-name">
            <span>{weather.name}</span>
            <sup>{weather.sys.country}</sup>
          </h2>
          <div className="city-temp">
            {Math.round(weather.main.temp)}
            <sup>&deg;C</sup>
          </div>
          <div className="info">
          <img className="city-icon" src={`https://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`} alt={weather.weather[0].description}/>
          <p>{weather.weather[0].description}</p>
        </div>
        </div>
      )}
    </div>
  );
}

export default App;