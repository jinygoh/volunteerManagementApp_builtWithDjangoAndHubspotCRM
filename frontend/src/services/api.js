/**
 * @file api.js
 * @description File Purpose: Centralizes all API communication for the frontend.
 *
 * This file acts as a service layer for making HTTP requests to our Django backend.
 * It uses the 'axios' library to create a pre-configured instance that can be
 * used throughout the application. This approach is beneficial because:
 * 1.  **Centralized Configuration**: The base URL and request headers are configured
 *     in one place. If the API domain changes, we only need to update it here.
 * 2.  **Code Reusability**: Instead of writing `axios.post(...)` in every
 *     component, we can just call a named function like `signup(data)`.
 * 3.  **Abstraction**: Components don't need to know the exact API endpoints (URLs).
 *     They just need to know which function to call from this file.
 *
 * @relationship
 * - This file is imported by most of the "Page" components (e.g., `DashboardPage.jsx`,
 *   `LoginPage.jsx`) and the `AuthContext.jsx` to perform API calls.
 * - It makes requests to the endpoints defined in the backend's `api_urls.py`
 *   and handled by `api_views.py`.
 */
import axios from 'axios';

// Line: Create a new 'axios' instance.
// We create a custom instance of axios so we can set default values for our project.
export const api = axios.create({
  // Line: Set the base URL for all requests made with this instance.
  // This means any request we make (e.g., to '/volunteers/') will automatically
  // be sent to '/api/volunteers/'. The '/api' prefix is important because the
  // frontend development server (Vite) is configured to proxy all '/api' requests
  // to the backend Django server running on port 8000.
  baseURL: '/api/',
});

// Line: Use an "interceptor" to modify outgoing requests.
// An interceptor is a function that axios calls BEFORE the request is actually sent.
// This allows us to do things like automatically adding an authentication token
// to every request that requires it.
api.interceptors.request.use(config => {
    // Line: Get the authentication tokens from the browser's local storage.
    // When the user logs in, the `AuthContext` saves the tokens here.
    const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;

    // Line: If tokens exist, add the 'access' token to the request's 'Authorization' header.
    if (authTokens) {
        // This is the standard format for sending a JWT (JSON Web Token).
        // The backend will see this header, validate the token, and identify the user.
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    // Line: Return the modified configuration for axios to use.
    return config;
});

/**
 * Function: signup
 * @description Sends a POST request to the public signup endpoint to create a new volunteer application.
 * @param {object} volunteerData - The data from the signup form (e.g., name, email).
 * @returns {Promise} The axios promise, which will resolve with the server's response or reject with an error.
 */
export const signup = (volunteerData) => {
  // Line: Make a POST request to the '/api/signup/' URL with the volunteer data.
  return api.post('signup/', volunteerData);
};

/**
 * Function: getVolunteers
 * @description Fetches the list of all volunteers from the backend.
 * This request requires admin authentication, which our interceptor handles automatically.
 * @returns {Promise} The axios promise.
 */
export const getVolunteers = () => {
  // Line: Make a GET request to the '/api/volunteers/' URL.
  return api.get('volunteers/');
};

/**
 * Function: approveVolunteer
 * @description Sends a request to the backend to approve a specific volunteer.
 * @param {number} id - The unique ID of the volunteer to approve.
 * @returns {Promise} The axios promise.
 */
export const approveVolunteer = (id) => {
  // Line: Make a POST request to a URL like '/api/volunteers/5/approve/'.
  return api.post(`volunteers/${id}/approve/`);
};

/**
 * Function: rejectVolunteer
 * @description Sends a request to the backend to reject a specific volunteer.
 * @param {number} id - The unique ID of the volunteer to reject.
 * @returns {Promise} The axios promise.
 */
export const rejectVolunteer = (id) => {
  // Line: Make a POST request to a URL like '/api/volunteers/5/reject/'.
  return api.post(`volunteers/${id}/reject/`);
};

/**
 * Function: deleteVolunteer
 * @description Sends a request to the backend to delete a specific volunteer.
 * @param {number} id - The unique ID of the volunteer to delete.
 * @returns {Promise} The axios promise.
 */
export const deleteVolunteer = (id) => {
  // Line: Make a DELETE request to a URL like '/api/volunteers/5/'.
  return api.delete(`volunteers/${id}/`);
};

/**
 * Function: updateVolunteer
 * @description Sends a request to update a volunteer's details.
 * @param {number} id - The ID of the volunteer to update.
 * @param {object} volunteerData - An object containing the new data for the volunteer.
 * @returns {Promise} The axios promise.
 */
export const updateVolunteer = (id, volunteerData) => {
  // Line: Make a PUT request to a URL like '/api/volunteers/5/' with the new data.
  return api.put(`volunteers/${id}/`, volunteerData);
};

/**
 * Function: uploadCsv
 * @description Uploads a CSV file of volunteers for batch processing.
 * @param {File} file - The CSV file object from a file input field.
 * @returns {Promise} The axios promise.
 */
export const uploadCsv = (file) => {
  // Line: Create a 'FormData' object. This is the standard way to send files in an HTTP request.
  const formData = new FormData();
  // Line: Add the file to the form data under the key 'file'. The backend will look for this key.
  formData.append('file', file);
  // Line: Make a POST request to the '/api/upload-csv/' URL with the form data.
  return api.post('upload-csv/', formData);
};

/**
 * Function: login
 * @description Sends a POST request to the `/api/token/` endpoint to get authentication tokens.
 * @param {object} credentials - An object with { username, password }.
 * @returns {Promise} The axios promise.
 */
export const login = (credentials) => {
  // Line: Make a POST request to the '/api/token/' URL. This is a standard endpoint
  // for the Simple JWT library used by the backend.
  return api.post('token/', credentials);
};

/**
 * Function: logout
 * @description Sends a POST request to log out the currently authenticated user.
 * Note: This is often a placeholder. True JWT logout is typically handled on the
 * client-side by simply deleting the stored tokens. A backend endpoint might be
_stubbed_
 * used to blacklist a refresh token if needed, but is not implemented here.
 * @returns {Promise} The axios promise.
 */
export const logout = () => {
  // Line: Make a POST request to '/api/logout/'.
  return api.post('logout/');
};

// Line: Export the configured axios instance as the default export.
// This allows other files to import it if they need to use axios directly
// with the same base configuration (e.g., for setting up response interceptors).
export default api;
