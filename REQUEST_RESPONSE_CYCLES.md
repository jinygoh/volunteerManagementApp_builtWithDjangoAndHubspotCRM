# Request-Response Cycles

This document provides a detailed, "fleshed out" description of the request-response cycles in the HopeHands application. Because the application uses a decoupled frontend (React) and backend (Django REST API), we have two primary types of cycles to consider.

---

## 1. Initial Application Load Cycle

This cycle describes what happens when a user first loads the application in their browser.

1.  **User's Browser:** The user navigates to the root URL, `http://127.0.0.1:5173/` (during development).
2.  **Vite Dev Server:** The frontend development server receives the request.
3.  **HTTP Response (HTML Shell):** The server responds with the main `index.html` file. This file is mostly empty; it's a "shell" that contains a `<div id="root"></div>` and `<script>` tags to load the React application's JavaScript bundles.
4.  **Browser Rendering:**
    - The browser parses the `index.html`.
    - It then makes additional requests to download the JavaScript files specified in the `<script>` tags.
5.  **React Application Bootstrap:**
    - Once the JavaScript is downloaded and executed, the React application starts.
    - `main.jsx` is the entry point, which renders the main `<App />` component into the `<div id="root">`.
    - The `App.jsx` component sets up `react-router-dom`. Based on the current URL (`/`), the router determines which page component to render first. In this case, it's the `<DashboardPage />`.
    - The initial UI of the application is now visible.

---

## 2. API Request-Response Cycle (Example: Admin Approving a Volunteer)

This cycle describes what happens when the frontend needs to communicate with the backend API. We'll use the "Approve Volunteer" feature as an example.

1.  **User Action (in the Browser):**
    - The admin is viewing the `DashboardPage`, which has already fetched and displayed a list of volunteers.
    - The admin finds a volunteer with a "pending" status and clicks the "Approve" button next to their name.
2.  **Frontend Event Handling (React):**
    - The `onClick` event on the button triggers the `handleApprove(volunteer.id)` function within the `DashboardPage.jsx` component.
3.  **Frontend API Service Call:**
    - The `handleApprove` function calls `approveVolunteer(id)` from our service module, `frontend/src/services/api.js`.
4.  **Asynchronous HTTP Request (Axios):**
    - The `approveVolunteer` function uses the `axios` instance to send an asynchronous `POST` request to the URL `/api/volunteers/{id}/approve/`.
    - The `axios` request interceptor (in `api.js`) automatically attaches the user's JWT access token to the `Authorization` header of this request.
5.  **Backend Processing (Django):**
    - The Django development server (running on port 8000) receives the `POST` request. The Vite proxy forwards the request from `http://127.0.0.1:5173/api/...` to `http://127.0.0.1:8000/api/...`.
    - **URL Routing:** Django's URL router matches the path to the `approve` custom action within the `VolunteerViewSet`.
    - **Permissions:** The `VolunteerViewSet` checks its `permission_classes`. Since it includes `IsAuthenticated`, DRF's `JWTAuthentication` class inspects the `Authorization` header, validates the token, and authenticates the user. The check passes.
    - **View Logic (`api_views.py`):** The `approve` method is executed.
        - It retrieves the `Volunteer` object from the database using the `id` from the URL.
        - It updates the object's status: `volunteer.status = 'approved'`.
        - It calls the `HubspotAPI` service to create the contact in HubSpot.
        - It saves the returned HubSpot ID to the `volunteer.hubspot_id` field.
        - It saves the updated `volunteer` object to the database.
    - **HTTP Response Preparation:** The view prepares a JSON response, like `{"status": "volunteer approved"}`, and sets the HTTP status code to 200 (OK).
6.  **HTTP Response (Django to Browser):**
    - The Django server sends the JSON response back to the user's browser.
7.  **Frontend Promise Resolution (React):**
    - The `Promise` returned by the `axios` `POST` request in `api.js` resolves successfully.
    - The `await approveVolunteer(id)` line in the `DashboardPage.jsx` component completes.
8.  **UI Update (React):**
    - The `handleApprove` function then calls `fetchVolunteers()` to get the latest data.
    - `fetchVolunteers()` makes another API call (`GET /api/volunteers/`).
    - When the new list arrives, the component's state is updated via `setVolunteers([...])`.
    - This state change triggers React to re-render the `DashboardPage` component. The updated list is displayed, and the volunteer who was just approved now shows an "approved" status, and their "Approve"/"Reject" buttons are gone.

---

This detailed breakdown illustrates the modern, asynchronous communication between a SPA frontend and a REST API backend.
