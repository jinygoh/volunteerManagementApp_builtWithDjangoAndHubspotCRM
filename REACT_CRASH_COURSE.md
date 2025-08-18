# React Frontend Crash Course

This guide provides a crash course on the key components of the React frontend for the HopeHands application.

## 1. Project Structure

The frontend code lives in the `frontend/` directory. It was bootstrapped with Vite, a modern frontend build tool.

-   **`frontend/src/`**: This is where all our source code lives.
-   **`frontend/src/pages/`**: Contains the top-level components for each "page" of the application (e.g., `DashboardPage.jsx`, `LoginPage.jsx`).
-   **`frontend/src/services/`**: Contains modules that handle external interactions, like our API calls.
-   **`frontend/src/App.jsx`**: The main component that sets up the application layout and routing.
-   **`frontend/src/main.jsx`**: The entry point of the application that renders the `App` component into the DOM.

## 2. Core Concepts: Components, State, and Props

React applications are built from reusable pieces of code called **components**. Each component is a JavaScript function that returns HTML-like code called JSX.

### Example: The `DashboardPage` Component

Let's look at the main admin dashboard component to understand the key concepts.

**File:** `frontend/src/pages/DashboardPage.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import { getVolunteers, approveVolunteer } from '../services/api';

const DashboardPage = () => {
  // 1. State: `useState` hook to store data
  const [volunteers, setVolunteers] = useState([]);

  // 2. Effect: `useEffect` hook to fetch data when the component loads
  useEffect(() => {
    fetchVolunteers();
  }, []); // Empty array means this runs once on mount

  const fetchVolunteers = async () => {
    const response = await getVolunteers();
    setVolunteers(response.data);
  };

  // 3. Event Handler: A function to handle user actions
  const handleApprove = async (id) => {
    await approveVolunteer(id);
    fetchVolunteers(); // Refresh data after action
  };

  // 4. JSX: The rendered output
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <table>
        {/* ... table structure ... */}
        <tbody>
          {volunteers.map((volunteer) => (
            <tr key={volunteer.id}>
              <td>{volunteer.first_name} {volunteer.last_name}</td>
              {/* ... other data ... */}
              <td>
                <button onClick={() => handleApprove(volunteer.id)}>Approve</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### Key Concepts Explained:

1.  **State (`useState`)**: `const [volunteers, setVolunteers] = useState([]);`
    -   State is data that a component "remembers".
    -   The `useState` hook declares a state variable. `volunteers` is the current value, and `setVolunteers` is the function you call to update it.
    -   Whenever you call `setVolunteers`, React will automatically re-render the component to reflect the new data.

2.  **Effects (`useEffect`)**: `useEffect(() => { ... }, []);`
    -   Effects let you perform "side effects" in your components, such as fetching data, setting up subscriptions, or manually changing the DOM.
    -   The code inside `useEffect` runs *after* the component has rendered.
    -   The dependency array (`[]`) at the end is crucial. An empty array means the effect runs only once when the component first mounts. This is perfect for initial data fetching.

3.  **Event Handlers**: `const handleApprove = async (id) => { ... }`
    -   These are regular JavaScript functions that are called in response to user events, like `onClick`.
    -   In our app, they typically call an API service function and then re-fetch data to update the UI.

4.  **JSX**: This is the syntax that lets us write HTML inside JavaScript. The `.map()` function is used to loop over the `volunteers` array in our state and create a table row `<tr>` for each one.

## 3. Communicating with the Backend

We do not put API-calling logic directly in our components. Instead, we centralize it in a **service** module.

**File:** `frontend/src/services/api.js`

```javascript
import axios from 'axios';

// Create a pre-configured axios instance
const api = axios.create({
  baseURL: '/api/',
  // ... other config
});

// Export a function for each API endpoint
export const getVolunteers = () => {
  return api.get('volunteers/');
};

export const approveVolunteer = (id) => {
  return api.post(`volunteers/${id}/approve/`);
};
```

-   **`axios`**: We use the `axios` library to make HTTP requests.
-   **Centralization**: Keeping all API calls in one place makes the code cleaner. If we ever need to change how we handle authentication or errors, we only need to do it in this one file.
-   **Usage**: Our components (like `DashboardPage.jsx`) simply `import { getVolunteers } from '../services/api';` and call these functions, without needing to know the specific details of the API URLs or HTTP methods.

This separation of concerns (UI in components, API calls in services) is a key pattern for building maintainable React applications.
