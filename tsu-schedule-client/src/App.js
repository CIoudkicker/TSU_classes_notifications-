import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import ScheduleTable from './components/scheduleTable';

function App() {
  return (
    <Router>
      <div className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/schedule" element={<ScheduleTable />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
