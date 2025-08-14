import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom';

import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';

const Layout = () => (
  <div>
    <header>
      <nav>
        <h1>HopeHands</h1>
        <ul>
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/signup">Volunteer Signup</Link></li>
          <li><Link to="/login">Admin Login</Link></li>
        </ul>
      </nav>
    </header>
    <hr />
    <main>
      <Outlet />
    </main>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="signup" element={<SignupPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
