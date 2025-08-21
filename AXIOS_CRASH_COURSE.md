# Axios API Service Crash Course

This document explains how the HopeHands React frontend communicates with the backend API. The project uses the `axios` library to handle all HTTP requests, but it does so in a highly organized and reusable way by creating a centralized API service.

---

## 1. The Centralized API Service

Instead of making `axios` calls directly from within React components, all API-related logic is centralized in a single file. This is a crucial design pattern for keeping the code clean, maintainable, and DRY (Don't Repeat Yourself).

**File:** `frontend/src/services/api.js`

This file does three main things:
1.  Creates a pre-configured `axios` instance.
2.  Adds logic to automatically handle authentication (JWT tokens).
3.  Exports a clean function for every API endpoint the application needs to call.

### a. Creating the `axios` Instance

```javascript
import axios from 'axios';

// Create an Axios instance with a base URL for all API requests.
const api = axios.create({
  baseURL: '/api/',
});
```
By creating an instance with a `baseURL`, we don't have to type `/api/` every time we make a call. We can just use relative paths like `volunteers/` or `signup/`.

### b. Automating Authentication with Interceptors

Interceptors are a powerful feature of `axios` that allow you to run code before a request is sent or after a response is received. This project uses them to completely automate the process of sending authentication tokens.

**Request Interceptor: Adding the Auth Token**
```javascript
// Use an interceptor to inject the JWT token into the request headers.
api.interceptors.request.use(config => {
    // 1. Get the token from localStorage
    const authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    if (authTokens) {
        // 2. If it exists, add it to the 'Authorization' header
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
});
```
This code runs **before every single request**. It automatically adds the `Authorization: Bearer <token>` header, so we never have to think about it when calling protected API endpoints.

**Response Interceptor: Refreshing Expired Tokens**
The service also includes a response interceptor that automatically handles the case where an access token has expired. It detects the `401 Unauthorized` error, uses the refresh token to get a new access token, and then seamlessly retries the original failed request. This provides a smooth user experience without forcing the admin to log in again.

### c. Exporting Clean Service Functions

Finally, the file exports simple, named functions for each specific API call.

```javascript
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
```
This creates a clean and easy-to-use API layer.

---

## 2. Using the API Service in Components

With the service file set up, using it inside a React component is very straightforward. The component doesn't need to know anything about `axios`, URLs, or authentication tokens.

**File:** `frontend/src/pages/DashboardPage.jsx`

```jsx
// Simplified for explanation
import React, { useState, useEffect } from 'react';
// 1. Import the specific functions you need
import { getVolunteers, approveVolunteer } from '../services/api';

const DashboardPage = () => {
  const [volunteers, setVolunteers] = useState([]);

  const fetchVolunteers = async () => {
    // 2. Call the function to get data
    const response = await getVolunteers();
    setVolunteers(response.data.results);
  };

  useEffect(() => {
    fetchVolunteers();
  }, []);

  const handleApprove = async (id) => {
    // 3. Call the function to perform an action
    await approveVolunteer(id);
    fetchVolunteers(); // Refresh the data
  };

  return (
    // ... JSX to display volunteers and buttons ...
  );
};
```

### How it Works:
1.  **Import**: The component imports only the specific API functions it needs (e.g., `getVolunteers`, `approveVolunteer`).
2.  **Call**: It calls these functions as if they were any other local function, using `async/await` to handle the asynchronous nature of API calls.
3.  **No Details**: The component remains clean and focused on its primary job of displaying the UI. It doesn't need to worry about implementation details like HTTP methods (`GET`, `POST`), full URLs, or authentication headers. If the API endpoint ever changes, we only need to update it in `api.js`, and all components using that function will work without any changes.
