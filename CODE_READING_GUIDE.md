# How to Read the Code: A Guide to Understanding the Flow

This guide provides a step-by-step process for reading and understanding the code of the HopeHands Volunteer Management application. The application follows a modern, decoupled architecture with a React frontend and a Django REST API backend.

## The Core Principle: Follow the User's Action from Frontend to Backend

For any feature, the flow generally follows this path:

**React Component -> API Service -> Django URL -> Django View**

Here's how to apply this principle to the two main user flows in the application.

---

### Flow 1: A New Volunteer Signs Up

This is the flow for a new volunteer submitting their application.

1.  **Start at the User Interface - `frontend/src/pages/SignupPage.jsx`:**
    *   A user visits the signup page. This component renders a form to collect the volunteer's details.
    *   The state of the form is managed by the `useState` hook.
    *   When the user clicks "Sign Up", the `handleSubmit` function is called.

2.  **Follow to the API Service - `frontend/src/services/api.js`:**
    *   The `handleSubmit` function in `SignupPage.jsx` calls the `signup(formData)` function from our API service.
    *   Open `api.js` and find the `signup` function.
    *   **Conclusion:** This function takes the form data and sends a `POST` request to the `/api/signup/` endpoint on our backend.

3.  **Jump to the Backend URL - `hopehands/volunteer/api_urls.py`:**
    *   The backend receives the request. Django's URL dispatcher looks for a match.
    *   Open `api_urls.py` and find the line: `path('signup/', api_views.VolunteerPublicCreateView.as_view(), name='volunteer-signup-api')`.
    *   **Conclusion:** The `/api/signup/` URL is handled by the `VolunteerPublicCreateView` class in `api_views.py`.

4.  **End at the Backend Logic - `hopehands/volunteer/api_views.py`:**
    *   Open `api_views.py` and find the `VolunteerPublicCreateView`. This is a generic `CreateAPIView` from Django REST Framework.
    *   It uses the `VolunteerSerializer` to validate the incoming data. If the data is valid, it creates a new `Volunteer` object in the database.
    *   Crucially, the new `Volunteer` object is automatically saved with its default `status` of `'pending'`. No HubSpot interaction happens at this stage.

---

### Flow 2: An Administrator Approves a Volunteer

This flow covers an admin logging in, viewing the volunteer list, and approving an application.

1.  **Login (`LoginPage.jsx` -> `api.js` -> `/api/login/` -> `LoginView`):**
    *   The admin submits their credentials on the `LoginPage`.
    *   This calls the `/api/login/` endpoint, which is handled by the `LoginView` in the backend.
    *   The `LoginView` uses Django's `authenticate` and `login` functions to create a session for the user, setting an `HttpOnly` session cookie in the browser.

2.  **Viewing the Dashboard (`DashboardPage.jsx` -> `api.js` -> `/api/volunteers/`):**
    *   After logging in, the user is redirected to the `DashboardPage`.
    *   The `useEffect` hook in this component calls the `getVolunteers()` function from our `api.js` service.
    *   `getVolunteers()` sends a `GET` request to `/api/volunteers/`. Because the browser automatically attaches the session cookie, the backend knows the user is authenticated.

3.  **Backend List View (`api_urls.py` -> `api_views.py`):**
    *   The `/api/volunteers/` URL is handled by the `VolunteerViewSet`.
    *   The viewset's `list` action queries the database for all `Volunteer` objects and returns them as a JSON list.

4.  **Admin Action (`DashboardPage.jsx` -> `api.js` -> `/api/volunteers/{id}/approve/`):**
    *   The `DashboardPage` component receives the list of volunteers and displays them in a table.
    *   For a "pending" volunteer, the admin clicks the "Approve" button. This calls the `handleApprove(id)` function.
    *   `handleApprove` calls the `approveVolunteer(id)` function from `api.js`, which sends a `POST` request to the `/api/volunteers/{id}/approve/` endpoint.

5.  **Backend Approval Logic (`api_views.py` -> `hubspot_api.py`):**
    *   The request is routed to the `approve` custom action inside the `VolunteerViewSet`.
    *   This action performs the core logic:
        1.  It finds the `Volunteer` in the database.
        2.  It changes the `volunteer.status` to `'approved'`.
        3.  It instantiates the `HubspotAPI` service and calls `create_contact()`.
        4.  It receives the new contact's ID from HubSpot and saves it to the `volunteer.hubspot_id` field.
        5.  It saves the updated volunteer object.

6.  **UI Update (`DashboardPage.jsx`):**
    *   After the `approveVolunteer` API call successfully completes, the `DashboardPage` calls `fetchVolunteers()` again to get the updated list from the backend.
    *   React re-renders the component, now showing the volunteer's status as "approved".

By following these flows, you can trace the full lifecycle of a request from a user interaction in the React frontend to the business logic on the Django backend.
