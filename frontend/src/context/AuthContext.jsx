/**
 * @file AuthContext.jsx
 * @description File Purpose: This file defines the "Authentication Context" for
 * the entire React application.
 *
 * What is a "Context"?
 * In React, data is usually passed from parent components to child components
 * via "props". However, for application-wide data like user authentication status,
 * passing props through every single component would be very tedious. This is called
 * "prop drilling".
 *
 * A "Context" provides a way to share values like these between components
 * without having to explicitly pass a prop through every level of the tree.
 *
 * This file creates a context for authentication, which holds the user's data,
 * their authentication tokens, and the login/logout functions. It also contains
 * the advanced logic for automatically refreshing authentication tokens.
 *
 * @relationship
 * - `main.jsx`: This file wraps the entire `<App />` component with the
 *   `<AuthProvider>` from this file, making the authentication context available
 *   to all other components.
 * - `api.js`: This file uses the `api` instance from `api.js` and adds a special
 *   "interceptor" to it for handling token refreshes.
 * - Any component that needs to know about the user or trigger login/logout will
 *   use the `useAuth()` hook defined at the bottom of this file.
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin, api } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

// Line: Create the context object.
// This object will hold the shared authentication data and functions.
const AuthContext = createContext(null);

/**
 * Component: AuthProvider
 * @description This is a special component that "provides" the authentication
 * context to all of its children. Any component nested inside `AuthProvider`
 * in the component tree will be able to access the `value` object defined below.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render (our entire app).
 * @returns {JSX.Element} The rendered provider component.
 */
export const AuthProvider = ({ children }) => {
  // --- Component State ---

  // Line: `authTokens` state: holds the JWT access and refresh tokens.
  // It's initialized with a function that runs once. This function tries to
  // load the tokens from the browser's `localStorage`. This makes the user's
  // session "persistent" - they will stay logged in even if they refresh the page.
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);

  // Line: `user` state: holds the user's information (like username, ID) that is
  // decoded from the JWT access token. Also initialized from localStorage.
  const [user, setUser] =useState(() => localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null);

  // Line: `useNavigate` is a hook from `react-router-dom` that gives us a function
  // to programmatically navigate the user to different pages.
  const navigate = useNavigate();

  /**
   * Function: login
   * @description Handles the user login process.
   * It calls the API to get tokens, then updates the state and local storage.
   * @param {object} credentials - The user's login credentials ({ username, password }).
   */
  const login = async (credentials) => {
    // Line: Call the login function from our api service.
    const response = await apiLogin(credentials);
    const data = response.data; // The response data contains the access and refresh tokens.
    // Line: Update the `authTokens` state with the new tokens.
    setAuthTokens(data);
    // Line: Decode the new access token to get the user's info and update the `user` state.
    setUser(jwtDecode(data.access));
    // Line: Save the new tokens to localStorage to persist the session.
    localStorage.setItem('authTokens', JSON.stringify(data));
    // Line: Navigate the user to the admin dashboard after a successful login.
    navigate('/admin/dashboard');
  };

  /**
   * Function: logout
   * @description Handles the user logout process.
   * It clears the state and removes the tokens from local storage.
   */
  const logout = () => {
    // Line: Clear the tokens and user from the component's state.
    setAuthTokens(null);
    setUser(null);
    // Line: Remove the tokens from localStorage.
    localStorage.removeItem('authTokens');
    // Line: Redirect the user to the login page.
    navigate('/login');
  };

  // --- Side Effect for Token Refresh Logic ---
  // This `useEffect` hook is the most complex part of this file. It sets up a
  // global "interceptor" on our `api` instance from `api.js`.
  useEffect(() => {
    // An interceptor "intercepts" requests or responses before they are handled further.
    // This is a RESPONSE interceptor.
    const interceptor = api.interceptors.response.use(
      // The first function handles SUCCESSFUL responses. We just pass them through.
      (response) => response,
      // The second function handles FAILED responses (errors).
      async (error) => {
        const originalRequest = error.config;
        // Line: Check if the error was a 401 (Unauthorized) and if we haven't already retried this request.
        if (error.response.status === 401 && !originalRequest._retry) {
          // Line: Mark this request as "retried" to prevent an infinite loop of retries.
          originalRequest._retry = true;

          // Line: Check if we have a refresh token available.
          if (authTokens?.refresh) {
            try {
              // Line: Make a request to the backend's refresh endpoint.
              const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
              const newTokens = response.data;

              // Line: If successful, update our state and localStorage with the new tokens.
              setAuthTokens(newTokens);
              setUser(jwtDecode(newTokens.access));
              localStorage.setItem('authTokens', JSON.stringify(newTokens));

              // Line: Update the header of the ORIGINAL failed request with the new access token.
              originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
              // Line: Retry the original request with the new token.
              return api(originalRequest);
            } catch (refreshError) {
              // Line: If the refresh token is also invalid or expired, the refresh will fail.
              console.error("Token refresh failed:", refreshError);
              // Line: Log the user out completely.
              logout();
              return Promise.reject(refreshError);
            }
          } else {
            // Line: If there was no refresh token to begin with, just log out.
            logout();
          }
        }
        // Line: For any other type of error, just return the error as is.
        return Promise.reject(error);
      }
    );

    // Line: This is a "cleanup" function. It runs when the AuthProvider component
    // is removed from the screen. It removes the interceptor to prevent memory leaks.
    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, [authTokens, logout]); // This effect depends on `authTokens` and `logout`.

  // Line: Define the "value" object that will be provided to all consuming components.
  const value = { user, login, logout, authTokens };

  // Line: Render the AuthContext.Provider, passing it the value.
  // `{children}` represents whatever components are nested inside AuthProvider.
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook: useAuth
 * @description A custom hook that simplifies accessing the AuthContext.
 * Instead of components needing to import and use `useContext(AuthContext)`
 * directly, they can just call `useAuth()`.
 * @returns {object} The authentication context value.
 */
export const useAuth = () => {
  return useContext(AuthContext);
};
