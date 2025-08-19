/**
 * @file api.js
 * @description This file configures and exports an Axios instance for making API calls to the Django backend.
 *
 * It includes an Axios interceptor that automatically attaches the JWT access token
 * to the Authorization header of every outgoing request, if a token is available
 * in local storage. This simplifies authentication for protected endpoints.
 *
 * It also exports a collection of functions that correspond to specific API endpoints,
 * providing a clean and reusable way to interact with the backend API from the
 * React components.
 */
import axios from 'axios';

// Create an Axios instance with a base URL for all API requests.
const api = axios.create({
  baseURL: '/api/',
});

// Use an interceptor to inject the JWT token into the request headers.
api.interceptors.request.use(config => {
    const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    if (authTokens) {
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
});

// Use a response interceptor to handle token refreshes.
api.interceptors.response.use(
  (response) => response, // Directly return successful responses.
  async (error) => {
    const originalRequest = error.config;
    // Check if the error is 401 and not a retry request.
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Mark the request as retried.

      const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;

      if (authTokens?.refresh) {
        try {
          // Attempt to refresh the token.
          const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
          const newTokens = response.data;

          // Store the new tokens.
          localStorage.setItem('authTokens', JSON.stringify(newTokens));

          // Update the authorization header for the original request.
          originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;

          // Retry the original request with the new token.
          return api(originalRequest);
        } catch (refreshError) {
          // If refresh fails, clear tokens and redirect to login.
          console.error("Token refresh failed:", refreshError);
          localStorage.removeItem('authTokens');
          window.location.href = '/login'; // Force redirect.
          return Promise.reject(refreshError);
        }
      } else {
        // If there's no refresh token, redirect to login.
        localStorage.removeItem('authTokens');
        window.location.href = '/login';
      }
    }
    // For all other errors, just reject the promise.
    return Promise.reject(error);
  }
);

/**
 * Sends a POST request to create a new volunteer application.
 * @param {object} volunteerData - The data from the signup form.
 * @returns {Promise} The axios promise for the request.
 */
export const signup = (volunteerData) => {
  return api.post('signup/', volunteerData);
};

/**
 * Fetches the list of all volunteers. Requires admin authentication.
 * @returns {Promise} The axios promise for the request.
 */
export const getVolunteers = () => {
  return api.get('volunteers/');
};

/**
 * Sends a request to approve a volunteer. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to approve.
 * @returns {Promise} The axios promise for the request.
 */
export const approveVolunteer = (id) => {
  return api.post(`volunteers/${id}/approve/`);
};

/**
 * Sends a request to reject a volunteer. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to reject.
 * @returns {Promise} The axios promise for the request.
 */
export const rejectVolunteer = (id) => {
  return api.post(`volunteers/${id}/reject/`);
};

/**
 * Sends a request to delete a volunteer. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to delete.
 * @returns {Promise} The axios promise for the request.
 */
export const deleteVolunteer = (id) => {
  return api.delete(`volunteers/${id}/`);
};

/**
 * Sends a request to update a volunteer's details. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to update.
 * @param {object} volunteerData - The new data for the volunteer.
 * @returns {Promise} The axios promise for the request.
 */
export const updateVolunteer = (id, volunteerData) => {
  return api.put(`volunteers/${id}/`, volunteerData);
};

/**
 * Uploads a CSV file of volunteers for batch processing. Requires admin authentication.
 * @param {File} file - The CSV file to upload.
 * @returns {Promise} The axios promise for the request.
 */
export const uploadCsv = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('upload-csv/', formData);
};

/**
 * Sends a POST request to the /api/token/ endpoint to log in an admin user.
 * @param {object} credentials - An object with { username, password }.
 * @returns {Promise} The axios promise for the request.
 */
export const login = (credentials) => {
  return api.post('token/', credentials);
};

/**
 * Sends a POST request to log out the currently authenticated user.
 * Note: This endpoint might not be implemented on the backend.
 * @returns {Promise} The axios promise for the request.
 */
export const logout = () => {
  return api.post('logout/');
};

export default api;
