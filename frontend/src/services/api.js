import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',
});

api.interceptors.request.use(config => {
    const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    if (authTokens) {
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
});

api.interceptors.response.use(response => response, async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;

        if (authTokens?.refresh) {
            try {
                const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                api.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
                originalRequest.headers['Authorization'] = 'Bearer ' + response.data.access;
                return api(originalRequest);
            } catch (refreshError) {
                // Handle failed refresh (e.g., redirect to login)
                console.error("Token refresh failed", refreshError);
                localStorage.removeItem('authTokens');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
    }
    return Promise.reject(error);
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

export const uploadCsv = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('upload-csv/', formData);
};

/**
 * Sends a POST request to log in an admin user.
 * @param {object} credentials - An object with { username, password }.
 * @returns {Promise} - The axios promise for the request.
 */
export const login = (credentials) => {
  return api.post('token/', credentials);
};

/**
 * Sends a POST request to log out the currently authenticated user.
 * @returns {Promise} - The axios promise for the request.
 */
export const logout = () => {
  return api.post('logout/');
};

export default api;
