/**
 * @file api.js
 * @description This file configures and exports an Axios instance for making API calls to the Django backend.
 *
 * It includes a request interceptor that automatically attaches the JWT access token
 * to the Authorization header of every outgoing request. The response interceptor
 * for handling token refreshes is managed in `src/context/AuthContext.jsx`.
 *
 * This file also exports a collection of functions that correspond to specific API
 * endpoints, providing a clean and reusable way to interact with the backend API
 * from the React components.
 */
import axios from 'axios';

// Create an Axios instance with a base URL for all API requests.
export const api = axios.create({
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
