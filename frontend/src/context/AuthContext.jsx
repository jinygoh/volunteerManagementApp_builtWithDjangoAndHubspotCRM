/**
 * @file AuthContext.jsx
 * @description This file defines the authentication context for the React application.
 *
 * It provides a way to share authentication state (like the user object and JWT tokens)
 * and functions (like login, logout, and token refresh) across all components
 * wrapped within the `AuthProvider`. This avoids the need to pass props down through
 * multiple levels of the component tree (prop drilling).
 */
import React, { createContext, useState, useContext } from 'react';
import { login as apiLogin } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

// Create the authentication context.
const AuthContext = createContext(null);

/**
 * The provider component that makes the authentication state and functions
 * available to all of its children.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render.
 * @returns {JSX.Element} The rendered provider component.
 */
export const AuthProvider = ({ children }) => {
  // State to hold the JWT tokens (access and refresh). Initialized from local storage.
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  // State to hold the decoded user object from the access token. Initialized from local storage.
  const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null);

  const navigate = useNavigate();

  /**
   * Handles the user login process.
   * It calls the API to get tokens, then updates the state and local storage.
   * @param {object} credentials - The user's login credentials ({ username, password }).
   */
  const login = async (credentials) => {
    const response = await apiLogin(credentials);
    const data = response.data;
    setAuthTokens(data);
    setUser(jwtDecode(data.access));
    localStorage.setItem('authTokens', JSON.stringify(data));
    navigate('/admin/dashboard');
  };

  /**
   * Handles the user logout process.
   * It clears the state and removes the tokens from local storage.
   */
  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  /**
   * Refreshes the JWT access token using the refresh token.
   * This is typically called by an Axios interceptor when a 401 error is received.
   */
  const refreshToken = async () => {
    try {
        const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
        const data = response.data;
        setAuthTokens(data);
        setUser(jwtDecode(data.access));
        localStorage.setItem('authTokens', JSON.stringify(data));
        return data;
    } catch (error) {
        console.error("Failed to refresh token", error);
        logout(); // Logout user if refresh fails
    }
  };

  // The value provided to the context consumers.
  const value = { user, login, logout, refreshToken, authTokens };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * A custom hook for consuming the AuthContext.
 * This makes it easy for any component to access the authentication state and functions.
 * @returns {object} The authentication context value.
 */
export const useAuth = () => {
  return useContext(AuthContext);
};
