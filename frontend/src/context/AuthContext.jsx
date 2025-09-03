/**
 * @file AuthContext.jsx
 * @description This file defines the authentication context for the React application.
 *
 * It provides a way to share authentication state (like the user object and JWT tokens)
 * and functions (like login and logout) across all components wrapped within the
 * `AuthProvider`. It also configures an Axios interceptor to handle automatic
 * JWT token refreshes, ensuring seamless authenticated sessions.
 */
import React, { createContext, useState, useContext } from 'react';
import { login as apiLogin } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";

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
  // State to hold the JWT token. Initialized from local storage.
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  // State to hold the decoded user object from the token. Initialized from local storage.
  const [user, setUser] = useState(() => {
    const storedTokens = localStorage.getItem('authTokens');
    if (storedTokens) {
      const parsedTokens = JSON.parse(storedTokens);
      return parsedTokens.token ? jwtDecode(parsedTokens.token) : null;
    }
    return null;
  });

  const navigate = useNavigate();

  /**
   * Handles the user login process.
   * It calls the API to get a token, then updates the state and local storage.
   * @param {object} credentials - The user's login credentials ({ username, password }).
   */
  const login = async (credentials) => {
    const response = await apiLogin(credentials);
    const data = response.data; // This is now { token: '...' }
    setAuthTokens(data);
    setUser(jwtDecode(data.token));
    localStorage.setItem('authTokens', JSON.stringify(data));
    navigate('/admin/dashboard');
  };

  /**
   * Handles the user logout process.
   * It clears the state and removes the token from local storage.
   */
  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  // The value provided to the context consumers.
  const value = { user, login, logout, authTokens };

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
