/**
 * @file App.jsx
 * @description The main component of the React application.
 *
 * This file sets up the application's routing using `react-router-dom` and
 * wraps the entire application in the `AuthProvider` to provide authentication
 * context to all child components. It defines the main layout, including the
 * navigation bar, and distinguishes between public and protected routes.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import UploadCsvPage from './pages/UploadCsvPage';
import ProtectedRoute from './components/ProtectedRoute';

/**
 * The main layout component for the application.
 * It includes the navigation bar and a container for the page content.
 * The navigation bar's links change based on the user's authentication status.
 * @returns {JSX.Element} The rendered layout component.
 */
const Layout = () => {
    const { user, logout } = useAuth();

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container">
                    <Link className="navbar-brand" to="/">HopeHands</Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            {/* Conditional rendering based on user authentication status */}
                            {user ? (
                                // Links for authenticated (admin) users
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/admin/dashboard">Dashboard</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/admin/upload-csv">Upload CSV</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/signup">Volunteer Signup Form</Link>
                                    </li>
                                    <li className="nav-item">
                                        <button className="btn btn-link nav-link" onClick={logout}>Logout</button>
                                    </li>
                                </>
                            ) : (
                                // Links for public (unauthenticated) users
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/signup">Volunteer Signup</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/login">Admin Login</Link>
                                    </li>
                                </>
                            )}
                        </ul>
                    </div>
                </div>
            </nav>
            {/* The Outlet component renders the matched child route's element */}
            <div className="container mt-4">
                <Outlet />
            </div>
        </>
    );
};

/**
 * The root component that sets up the application's router and routes.
 * @returns {JSX.Element} The rendered App component.
 */
function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* All routes use the main Layout component */}
          <Route element={<Layout />}>
            {/* Public routes that do not require authentication */}
            <Route path="/" element={<SignupPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />

            {/* Protected routes that require admin authentication */}
            <Route element={<ProtectedRoute />}>
              <Route path="/admin/dashboard" element={<DashboardPage />} />
              <Route path="/admin/upload-csv" element={<UploadCsvPage />} />
            </Route>
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
