/**
 * @file LoginPage.jsx
 * @description This component renders the administrator login page.
 *
 * It provides a form for an admin to enter their username and password.
 * On submission, it calls the `login` function from the `AuthContext` to
 * authenticate the user and retrieve JWT tokens. It also handles the
 * display of login errors.
 */
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

/**
 * The main component for the admin login page.
 * @returns {JSX.Element} The rendered login page.
 */
const LoginPage = () => {
  // State for form inputs and error messages.
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Get the login function from the authentication context.
  const { login } = useAuth();

  /**
   * Handles the form submission for logging in.
   * @param {React.FormEvent} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Attempt to log in with the provided credentials.
      await login({ username, password });
      // On success, the AuthContext will handle navigation to the dashboard.
    } catch (err) {
      setError('Failed to log in. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="form-container">
          <h1 className="text-center mb-4">Admin Login</h1>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                className="form-control"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="d-grid">
                <button type="submit" className="btn btn-primary">Login</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
