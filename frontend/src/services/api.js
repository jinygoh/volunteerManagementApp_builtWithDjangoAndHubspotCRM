import axios from 'axios';

// Create an axios instance
const api = axios.create({
  baseURL: '/api/', // The proxy will handle redirecting this to the Django backend
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: true,
});

export const signup = (volunteerData) => {
  return api.post('signup/', volunteerData);
};

export const getVolunteers = () => {
  return api.get('volunteers/');
};

export const approveVolunteer = (id) => {
  return api.post(`volunteers/${id}/approve/`);
};

export const rejectVolunteer = (id) => {
  return api.post(`volunteers/${id}/reject/`);
};

// We still need a login function.
// The default Django login view is form-based, not API-based.
// We will need to create an API login endpoint.
// For now, we will assume one exists for the purpose of frontend structure.
export const login = (credentials) => {
  // This will likely need to be adjusted once the backend endpoint is created
  // For now, let's assume it's a simple post to /api/login/
  return api.post('login/', credentials);
};

export default api;
