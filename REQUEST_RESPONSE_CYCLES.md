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

---

## 3. API Cycle: Admin Login

This cycle describes how an administrator logs in to the application.

1.  **User Action (in Browser):** The admin navigates to the `/login` page and submits the login form with their username and password.
2.  **Frontend Event Handling (React):**
    - The `onSubmit` event on the form in `LoginPage.jsx` triggers the `login(credentials)` function from the `AuthContext`.
3.  **Frontend API Service Call:**
    - The `login` function in `AuthContext.jsx` calls the `login(credentials)` function from `frontend/src/services/api.js`.
4.  **Asynchronous HTTP Request (Axios):**
    - The `api.js` service sends a `POST` request to the backend URL `/api/token/`. This is the standard endpoint for the Simple JWT library. The request body contains the user's credentials.
5.  **Backend Processing (Django):**
    - Django's URL router maps `/api/token/` to the `TokenObtainPairView` from the Simple JWT library.
    - This view authenticates the user against the database.
    - If the credentials are valid, the view generates a new pair of JWTs: a short-lived **access token** and a long-lived **refresh token**.
6.  **HTTP Response (Django to Browser):**
    - The backend sends a 200 (OK) response containing the access and refresh tokens in a JSON object.
7.  **Frontend Promise Resolution (React):**
    - The `Promise` returned by the `axios` `POST` request resolves successfully.
    - The `await apiLogin(credentials)` line in `AuthContext.jsx` completes.
8.  **UI and State Update (React):**
    - The `login` function in `AuthContext` updates its internal state with the new tokens and the decoded user data.
    - It saves the tokens to the browser's `localStorage` to keep the user logged in across page refreshes.
    - It programmatically navigates the user to the `/admin/dashboard` page.

---

## 4. API Cycle: Reject a Volunteer

This cycle is the counterpart to the "Approve" cycle.

1.  **User Action (in Browser):** An admin on the `DashboardPage` clicks the "Reject" button for a pending volunteer.
2.  **Frontend Event Handling (React):** The `onClick` event triggers the `handleReject(volunteer.id)` function in `DashboardPage.jsx`.
3.  **Frontend API Service Call:** The handler calls `rejectVolunteer(id)` from `frontend/src/services/api.js`.
4.  **Asynchronous HTTP Request (Axios):** A `POST` request is sent to `/api/volunteers/{id}/reject/`. The request interceptor attaches the admin's JWT access token to the header.
5.  **Backend Processing (Django):**
    - The URL is routed to the `reject` custom action in the `VolunteerViewSet`.
    - The `IsAuthenticated` permission checks the JWT and confirms the user is an admin.
    - The `reject` method retrieves the `Volunteer` object.
    - It changes the volunteer's status to `volunteer.status = 'rejected'`.
    - It saves the updated volunteer object to the database.
    - **Note:** Unlike the approve action, no communication with HubSpot occurs here.
6.  **HTTP Response (Django to Browser):** The backend sends a 200 (OK) response, like `{"status": "volunteer rejected"}`.
7.  **Frontend Promise Resolution (React):** The `await rejectVolunteer(id)` call completes.
8.  **UI Update (React):** The `handleReject` function calls `fetchVolunteers()` again to get the latest data, which triggers a re-render of the dashboard to show the "rejected" status.

---

## 5. API Cycle: Delete a Volunteer (with HubSpot Sync)

This cycle shows how deleting a user from our app also removes them from HubSpot.

1.  **User Action (in Browser):** An admin on the `DashboardPage` clicks the "Delete" button for any volunteer. A browser confirmation dialog appears and the admin confirms.
2.  **Frontend Event Handling (React):** The `onClick` event triggers `handleDelete(volunteer.id)`.
3.  **Frontend API Service Call:** The handler calls `deleteVolunteer(id)` from `frontend/src/services/api.js`.
4.  **Asynchronous HTTP Request (Axios):** A `DELETE` request is sent to `/api/volunteers/{id}/`. The admin's JWT is attached.
5.  **Backend Processing (Django):**
    - The request is routed to the `destroy` method in the `VolunteerViewSet`.
    - The method retrieves the `Volunteer` object.
    - It checks if `volunteer.hubspot_id` exists.
    - **HubSpot API Call:** If a `hubspot_id` exists, the backend makes a **server-to-server API call** to HubSpot's API, requesting to "archive" (delete) the contact with that ID.
    - After the HubSpot call completes, the method proceeds to delete the `Volunteer` object from the local database.
6.  **HTTP Response (Django to Browser):** The backend sends a 204 (No Content) response, which is standard for a successful deletion.
7.  **Frontend Promise Resolution (React):** The `await deleteVolunteer(id)` call completes.
8.  **UI Update (React):** The component re-fetches the volunteer list, and the deleted volunteer is no longer present.

---

## 6. API Cycle: Update a Volunteer (with HubSpot Sync)

This cycle shows how editing a user in our app also updates them in HubSpot.

1.  **User Action (in Browser):** An admin edits a volunteer's details on the `EditVolunteerPage` and clicks "Save".
2.  **Frontend Event Handling (React):** The `onSubmit` event triggers `handleUpdate(volunteerData)`.
3.  **Frontend API Service Call:** The handler calls `updateVolunteer(id, volunteerData)` from `api.js`.
4.  **Asynchronous HTTP Request (Axios):** A `PUT` request is sent to `/api/volunteers/{id}/` with the updated volunteer data in the request body. The admin's JWT is attached.
5.  **Backend Processing (Django):**
    - The request is routed to the `update` method in the `VolunteerViewSet`.
    - The method validates the incoming data and updates the corresponding `Volunteer` object in the local database.
    - It then checks if the updated volunteer has a `hubspot_id`.
    - **HubSpot API Call:** If a `hubspot_id` exists, the backend makes a **server-to-server API call** to HubSpot's API, requesting to update the contact's properties with the new data.
6.  **HTTP Response (Django to Browser):** The backend sends a 200 (OK) response with the updated volunteer data.
7.  **Frontend Promise Resolution (React):** The `await updateVolunteer(...)` call completes.
8.  **UI Update (React):** The user is typically navigated back to the dashboard, which will show the updated information.

---

## 7. API Cycle: New Volunteer Signup (Public)

1.  **User Action (in Browser):** A new, prospective volunteer fills out the public signup form and clicks "Submit".
2.  **Frontend Event Handling (React):** The `onSubmit` event on the form in `SignupPage.jsx` triggers a handler function.
3.  **Frontend API Service Call:** The handler calls `signup(volunteerData)` from `api.js`.
4.  **Asynchronous HTTP Request (Axios):** A `POST` request is sent to `/api/signup/`. This is a public endpoint, so no authentication token is needed or sent.
5.  **Backend Processing (Django):**
    - The URL is routed to the `VolunteerPublicCreateView`.
    - This view uses the `VolunteerSerializer` to validate the submitted data.
    - If valid, it creates a new `Volunteer` object in the database. The status is automatically set to the default value of `'pending'`.
6.  **HTTP Response (Django to Browser):** The backend sends a 201 (Created) response containing the data for the newly created volunteer.
7.  **Frontend Promise Resolution (React):** The `await signup(...)` call completes.
8.  **UI Update (React):** The `SignupPage.jsx` component displays a "Thank you for your application!" message to the user.

---

## 8. API Cycle: CSV Bulk Upload (with HubSpot Sync)

1.  **User Action (in Browser):** An admin on the `UploadCsvPage` selects a CSV file and clicks "Upload".
2.  **Frontend Event Handling (React):** The `onSubmit` event triggers the `handleUpload(file)` function.
3.  **Frontend API Service Call:** The handler calls `uploadCsv(file)` from `api.js`.
4.  **Asynchronous HTTP Request (Axios):** A `POST` request is sent to `/api/upload-csv/`. The request body is `multipart/form-data` to handle the file upload. The admin's JWT is attached.
5.  **Backend Processing (Django):**
    - The request is routed to the `VolunteerCSVUploadAPIView`.
    - The backend parses the CSV file, reading each row.
    - It creates a list of new `Volunteer` objects, setting their status directly to `'approved'`.
    - It performs a `bulk_create` operation to efficiently insert all new volunteers into the local database.
    - **HubSpot API Call:** The backend prepares a list of all the new contacts and makes a single **server-to-server batch API call** to HubSpot to create all of them at once.
    - After HubSpot responds, the backend updates the newly created local volunteer records with their corresponding `hubspot_id`s.
6.  **HTTP Response (Django to Browser):** The backend sends a 201 (Created) response with a status message, e.g., `{"status": "50 volunteers created locally. 50 synced to HubSpot."}`.
7.  **Frontend Promise Resolution (React):** The `await uploadCsv(...)` call completes.
8.  **UI Update (React):** The `UploadCsvPage` displays the success message from the backend to the admin.

---

## 9. API Cycle: Fetch Visualization Data

1.  **User Action (in Browser):** An admin navigates to the `VisualizationPage`.
2.  **Frontend Event Handling (React):** The `VisualizationPage.jsx` component mounts.
3.  **Side Effect (`useEffect`):** A `useEffect` hook runs, which calls a function to fetch the chart data.
4.  **Asynchronous HTTP Request (Axios):** A `GET` request is sent to `/api/visualizations/`. The admin's JWT is attached.
5.  **Backend Processing (Django):**
    - The URL is routed to the `VolunteerVisualizationView`.
    - The view performs a database query to group volunteers by their `preferred_volunteer_role` and count the number of volunteers in each role.
6.  **HTTP Response (Django to Browser):** The backend sends a 200 (OK) response containing the aggregated data, e.g., `[{"preferred_volunteer_role": "Events", "count": 15}, ...]`.
7.  **Frontend Promise Resolution (React):** The `Promise` from the `axios` `GET` request resolves.
8.  **UI Update (React):** The component updates its state with the received data, and the charting library uses this data to render the bar chart.

---

## 10. API Cycle: Automatic Token Refresh

This cycle is special because it's not directly triggered by a user action, but rather by another API call failing.

1.  **Initial State:** An admin is logged in. Their short-lived JWT **access token** has just expired. Their long-lived **refresh token** is still valid.
2.  **User Action:** The admin performs any action that requires authentication (e.g., clicks on the dashboard to refresh the volunteer list).
3.  **Asynchronous HTTP Request (Axios):** The frontend sends a request (e.g., `GET /api/volunteers/`) with the **expired** access token in the `Authorization` header.
4.  **Backend Response (401 Unauthorized):**
    - The Django backend receives the request, inspects the token, sees that it's expired, and immediately rejects the request with a **401 Unauthorized** error response.
5.  **Frontend Interceptor Triggered (React):**
    - The `axios` response interceptor, configured in `AuthContext.jsx`, catches this specific 401 error before the original component's `catch` block is executed.
    - The interceptor pauses the original request.
6.  **Token Refresh Request (Axios):**
    - The interceptor's logic sends a **new `POST` request** to the `/api/token/refresh/` endpoint. The body of this request contains the valid **refresh token**.
7.  **Backend Token Refresh (Django):**
    - The `TokenRefreshView` from the Simple JWT library receives the refresh token.
    - It verifies the refresh token. If valid, it generates a **brand new access token**.
    - It sends a 200 (OK) response containing the new access token.
8.  **Frontend Interceptor Logic (React):**
    - The interceptor receives the new access token.
    - It updates the `AuthContext` state and `localStorage` with the new token.
    - It takes the **original, failed request** (the `GET /api/volunteers/` call) and updates its `Authorization` header with the new access token.
    - It then **retries** the original request.
9.  **Backend Final Response:** The backend receives the retried request. This time, the access token is valid, so it processes the request normally and returns a 200 (OK) response with the volunteer list.
10. **UI Update:** The original component's `await` call finally completes successfully, and the UI is updated as intended. The user is unaware this entire refresh process happened.
