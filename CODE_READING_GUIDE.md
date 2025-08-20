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

1.  **Login (`LoginPage.jsx` -> `api.js` -> `/api/token/`):**
    *   The admin submits their credentials on the `LoginPage`.
    *   This calls the `login()` function in `api.js`, which sends a `POST` request to the `/api/token/` endpoint.
    *   This endpoint is handled by `djangorestframework-simplejwt`'s `TokenObtainPairView`, which validates the credentials.
    *   If successful, the backend returns a pair of JSON Web Tokens (JWT): an `access` token and a `refresh` token. The frontend stores these tokens in local storage.

2.  **Viewing the Dashboard (`DashboardPage.jsx` -> `api.js` -> `/api/volunteers/`):**
    *   After logging in, the user is redirected to the `DashboardPage`.
    *   The `useEffect` hook in this component calls the `getVolunteers()` function from our `api.js` service.
    *   `getVolunteers()` sends a `GET` request to `/api/volunteers/`. The `axios` interceptor in `api.js` automatically attaches the stored JWT access token to the `Authorization` header of the request.

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

---

## Additional Flows to Explore

### Flow 3: Admin Bulk-Uploads Volunteers via CSV

This flow covers an admin using the CSV upload feature to perform a batch import.

1.  **Start at the UI - `frontend/src/pages/UploadCsvPage.jsx`:**
    *   An admin navigates to the "Upload CSV" page.
    *   They select a CSV file and click "Upload". This calls the `handleUpload` function.

2.  **Follow to the API Service - `frontend/src/services/api.js`:**
    *   The `handleUpload` function calls `uploadCsv(file)`, which sends a `POST` request with `multipart/form-data` to the `/api/upload-csv/` endpoint.

3.  **End at the Backend Logic - `hopehands/volunteer/api_views.py`:**
    *   The `/api/upload-csv/` URL is handled by the `VolunteerCSVUploadAPIView`.
    *   This view reads the CSV file, and for each row, it creates a `Volunteer` object with the status `'approved'`. It uses `bulk_create` for efficiency.
    *   It then calls the `hubspot_api.batch_create_contacts` method to sync all the new volunteers to HubSpot in a single API call.
    *   Finally, it updates the newly created local `Volunteer` records with their `hubspot_id` returned from the batch API call.

### Flow 4: Admin Views Volunteer Data Visualization

This flow covers an admin viewing the new data visualization chart.

1.  **Start at the UI - `frontend/src/pages/VisualizationPage.jsx`:**
    *   The admin navigates to the "Visualizations" page.
    *   The `useEffect` hook in this component immediately calls a function to fetch the visualization data.

2.  **Follow to the API Service - `frontend/src/services/api.js`:**
    *   The fetch function in the component calls a generic `api.get()` method (from the `axios` instance) on the `/api/visualizations/volunteer-roles/` endpoint.

3.  **End at the Backend Logic - `hopehands/volunteer/api_views.py`:**
    *   The `/api/visualizations/volunteer-roles/` URL is handled by the `VolunteerVisualizationView`.
    *   This view queries the `Volunteer` model, groups the records by `preferred_volunteer_role`, and returns a JSON array containing each role and the count of volunteers for that role.

4.  **UI Renders the Chart - `frontend/src/pages/VisualizationPage.jsx`:**
    *   The component receives the aggregated data.
    *   It transforms this data into the format required by the `react-chartjs-2` library.
    *   It then renders a `<Bar>` component, displaying the data as a bar chart.
