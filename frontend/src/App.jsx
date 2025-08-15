import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom';

import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';

const Layout = () => (
  <>
    <nav className="navbar navbar-expand-lg navbar-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">HopeHands</Link>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link className="nav-link" to="/signup">Volunteer Signup</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/">Volunteer List</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/login">Admin Login</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div className="container mt-4">
      <Outlet />
    </div>
  </>
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
