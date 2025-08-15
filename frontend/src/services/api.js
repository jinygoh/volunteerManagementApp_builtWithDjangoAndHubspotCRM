import axios from 'axios';

/**
 * Creates a pre-configured instance of axios.
 * The baseURL is set to '/api/', which will be handled by the Vite proxy
 * in development to redirect to the Django backend (e.g., http://127.0.0.1:8000/api/).
 * It's also configured to handle Django's CSRF tokens automatically.
 */
const api = axios.create({
  baseURL: '/api/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: true,
});

/**
 * Sends a POST request to create a new volunteer application.
 * @param {object} volunteerData - The data from the signup form.
 * @returns {Promise} - The axios promise for the request.
 */
export const signup = (volunteerData) => {
  return api.post('signup/', volunteerData);
};

/**
 * Fetches the list of all volunteers. Requires admin authentication.
 * @returns {Promise} - The axios promise for the request.
 */
export const getVolunteers = () => {
  return api.get('volunteers/');
};

/**
 * Sends a request to approve a volunteer. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to approve.
 * @returns {Promise} - The axios promise for the request.
 */
export const approveVolunteer = (id) => {
  return api.post(`volunteers/${id}/approve/`);
};

/**
 * Sends a request to reject a volunteer. Requires admin authentication.
 * @param {number} id - The ID of the volunteer to reject.
 * @returns {Promise} - The axios promise for the request.
 */
export const rejectVolunteer = (id) => {
  return api.post(`volunteers/${id}/reject/`);
};

/**
 * Sends a POST request to log in an admin user.
 * @param {object} credentials - An object with { username, password }.
 * @returns {Promise} - The axios promise for the request.
 */
export const login = (credentials) => {
  return api.post('login/', credentials);
};

/**
 * Sends a POST request to log out the currently authenticated user.
 * @returns {Promise} - The axios promise for the request.
 */
export const logout = () => {
  return api.post('logout/');
};

export default api;
