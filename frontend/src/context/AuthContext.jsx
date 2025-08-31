/**
 * @file AuthContext.jsx
 * @description This file defines the authentication context for the React application.
 *
 * It provides a way to share authentication state (like the user object and JWT tokens)
 * and functions (like login and logout) across all components wrapped within the
 * `AuthProvider`. It also configures an Axios interceptor to handle automatic
 * JWT token refreshes, ensuring seamless authenticated sessions.
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin, api } from '../services/api';
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

  // This useEffect hook sets up a global Axios response interceptor to handle
  // JWT token refreshes automatically.
  // When an API call returns a 401 Unauthorized error, the interceptor
  // attempts to use the refresh token to get a new access token. If successful,
  // it updates the authentication state and local storage, and then retries the
  // original failed request with the new token. If the refresh fails, it logs
  // the user out.
  // The interceptor is cleaned up when the AuthProvider unmounts.
  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          if (authTokens?.refresh) {
            try {
              const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
              const newTokens = response.data;

              setAuthTokens(newTokens);
              setUser(jwtDecode(newTokens.access));
              localStorage.setItem('authTokens', JSON.stringify(newTokens));

              originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
              return api(originalRequest);
            } catch (refreshError) {
              console.error("Token refresh failed:", refreshError);
              logout();
              return Promise.reject(refreshError);
            }
          } else {
            logout();
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, [authTokens, logout]);

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
