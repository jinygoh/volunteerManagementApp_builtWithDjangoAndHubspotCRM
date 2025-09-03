# How to Read the Code: A Guide to Understanding the Flow

This guide provides a step-by-step process for reading and understanding the code of the HopeHands Volunteer Management application. The application follows a modern, decoupled architecture with a React frontend and a Spring Boot REST API backend.

## The Core Principle: Follow the User's Action from Frontend to Backend

For any feature, the flow generally follows this path:

**React Component -> API Service -> Spring Boot Controller -> Spring Boot Service**

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
    *   **Conclusion:** This function takes the form data and sends a `POST` request to the `/api/signup` endpoint on our backend.

3.  **Jump to the Backend Controller - `backend/src/main/java/com/hopehands/controller/VolunteerController.java`:**
    *   The backend receives the request. Spring Boot's dispatcher servlet routes the request to the correct controller method based on the `@RequestMapping` and `@PostMapping` annotations.
    *   **Conclusion:** The `/api/signup` URL is handled by the `signup` method in the `VolunteerController`.

4.  **End at the Backend Logic - `backend/src/main/java/com/hopehands/service/VolunteerService.java`:**
    *   The `signup` method in the `VolunteerController` calls the `createVolunteer` method in the `VolunteerService`.
    *   The `createVolunteer` method sets the default status to "pending" and saves the new `Volunteer` object to the database using the `VolunteerRepository`.

---

### Flow 2: An Administrator Approves a Volunteer

This flow covers an admin logging in, viewing the volunteer list, and approving an application.

1.  **Login (`LoginPage.jsx` -> `api.js` -> `/api/token`):**
    *   The admin submits their credentials on the `LoginPage`.
    *   This calls the `login()` function in `api.js`, which sends a `POST` request to the `/api/token` endpoint.
    *   This endpoint is handled by the `AuthController`, which uses Spring Security's `AuthenticationManager` to validate the credentials.
    *   If successful, the backend returns a JWT. The frontend stores this token in local storage.

2.  **Viewing the Dashboard (`DashboardPage.jsx` -> `api.js` -> `/api/volunteers`):**
    *   After logging in, the user is redirected to the `DashboardPage`.
    *   The `useEffect` hook in this component calls the `getVolunteers()` function from our `api.js` service.
    *   `getVolunteers()` sends a `GET` request to `/api/volunteers`. The `axios` interceptor in `api.js` automatically attaches the stored JWT access token to the `Authorization` header of the request.

3.  **Backend List View (`VolunteerController.java` -> `VolunteerService.java`):**
    *   The `/api/volunteers` URL is handled by the `getVolunteers` method in the `VolunteerController`.
    *   This method calls the `getVolunteers` method in the `VolunteerService`, which queries the database for all `Volunteer` objects and returns them.

4.  **Admin Action (`DashboardPage.jsx` -> `api.js` -> `/api/volunteers/{id}/approve`):**
    *   The `DashboardPage` component receives the list of volunteers and displays them in a table.
    *   For a "pending" volunteer, the admin clicks the "Approve" button. This calls the `handleApprove(id)` function.
    *   `handleApprove` calls the `approveVolunteer(id)` function from `api.js`, which sends a `POST` request to the `/api/volunteers/{id}/approve` endpoint.

5.  **Backend Approval Logic (`VolunteerController.java` -> `VolunteerService.java`):**
    *   The request is routed to the `approveVolunteer` method in the `VolunteerController`.
    *   This method calls the `approveVolunteer` method in the `VolunteerService`, which finds the `Volunteer` in the database, changes the status to "approved", and saves the updated object.

6.  **Admin Action (Update):**
    *   The admin clicks the "Edit" button for a volunteer. This navigates them to the `EditVolunteerPage`.
    *   After changing the data and clicking "Save", the `handleSubmit` function calls `updateVolunteer(id, data)` from `api.js`.
    *   This sends a `PUT` request to `/api/volunteers/{id}`.
    *   The backend's `updateVolunteer` method handles the request.

7.  **Admin Action (Delete):**
    *   The admin clicks the "Delete" button for a volunteer.
    *   The `handleDelete(id)` function in `DashboardPage.jsx` calls `deleteVolunteer(id)` from `api.js`.
    *   This sends a `DELETE` request to `/api/volunteers/{id}`.
    *   The backend's `deleteVolunteer` method handles this.

8.  **UI Update (`DashboardPage.jsx`):**
    *   After the `approveVolunteer` API call successfully completes, the `DashboardPage` calls `fetchVolunteers()` again to get the updated list from the backend.
    *   React re-renders the component, now showing the volunteer's status as "approved".

By following these flows, you can trace the full lifecycle of a request from a user interaction in the React frontend to the business logic on the Spring Boot backend.

---

## Additional Flows to Explore

### Flow 3: Admin Bulk-Uploads Volunteers via CSV

This flow covers an admin using the CSV upload feature to perform a batch import.

1.  **Start at the UI - `frontend/src/pages/UploadCsvPage.jsx`:**
    *   An admin navigates to the "Upload CSV" page.
    *   They select a CSV file and click "Upload". This calls the `handleUpload` function.

2.  **Follow to the API Service - `frontend/src/services/api.js`:**
    *   The `handleUpload` function calls `uploadCsv(file)`, which sends a `POST` request with `multipart/form-data` to the `/api/upload-csv` endpoint.

3.  **End at the Backend Logic - `VolunteerController.java` -> `VolunteerService.java`:**
    *   The `/api/upload-csv` URL is handled by the `uploadCsv` method in the `VolunteerController`.
    *   This method calls the `uploadCsv` method in the `VolunteerService`, which reads the CSV file and creates `Volunteer` objects with the status "approved".

### Flow 4: Admin Views Volunteer Data Visualization

This flow covers an admin viewing the new data visualization chart.

1.  **Start at the UI - `frontend/src/pages/VisualizationPage.jsx`:**
    *   The admin navigates to the "Visualizations" page.
    *   The `useEffect` hook in this component immediately calls a function to fetch the visualization data.

2.  **Follow to the API Service - `frontend/src/services/api.js`:**
    *   The fetch function in the component calls a generic `api.get()` method (from the `axios` instance) on the `/api/visualizations/volunteer-roles` endpoint.

3.  **End at the Backend Logic - `VolunteerController.java` -> `VolunteerService.java`:**
    *   The `/api/visualizations/volunteer-roles` URL is handled by the `getRoleCounts` method in the `VolunteerController`.
    *   This method calls the `getRoleCounts` method in the `VolunteerService`, which queries the `Volunteer` model and returns aggregated data.

4.  **UI Renders the Chart - `frontend/src/pages/VisualizationPage.jsx`:**
    *   The component receives the aggregated data.
    *   It transforms this data into the format required by the `react-chartjs-2` library.
    *   It then renders a `<Bar>` component, displaying the data as a bar chart.
