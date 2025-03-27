import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Schedules = () => {
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/schedules/')
      .then(response => setSchedules(response.data))
      .catch(error => console.error('Error fetching schedules:', error));
  }, []);

  return (
    <div className="container mt-4">
      <h2>Schedules</h2>
      <ul className="list-group">
        {schedules.map(schedule => (
          <li key={schedule.id} className="list-group-item">
            {schedule.title} - {schedule.instructor} ({new Date(schedule.start_time).toLocaleString()})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Schedules;
