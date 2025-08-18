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
    // Retrieve the token from local storage.
    const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    // If a token exists, add it to the Authorization header.
    if (authTokens) {
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
});

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
