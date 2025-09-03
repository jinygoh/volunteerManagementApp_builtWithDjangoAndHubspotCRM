# Architecture Notes

This document contains notes and explanations about key architectural and design decisions in the HopeHands Volunteer Management application.

---

## High-Level Architecture

The application is designed as a modern, decoupled web application with two main parts:

1.  **An Express.js REST API Backend**: Serves as the data and logic layer.
2.  **A React Single-Page Application (SPA) Frontend**: Provides the user interface.

This separation of concerns allows for independent development, testing, and deployment of the backend and frontend.

### Express.js Backend

The backend is built with Node.js and the Express.js framework. It is responsible for:

-   **Data Persistence**: It uses a MongoDB database, managed via the Mongoose ODM (Object Data Modeling) library, to store all volunteer applications. The `models/Volunteer.js` and `models/User.js` schemas are the core of the data structure.
-   **Business Logic**: It contains the core business logic for the volunteer approval workflow.
-   **Serving a REST API**: It exposes a RESTful API that allows the frontend to perform all necessary actions, including:
    -   Publicly creating new volunteer applications.
    -   Authenticating administrators using JSON Web Tokens (JWT).
    -   Performing CRUD (Create, Read, Update, Delete) operations on volunteer records.
    -   Approving and rejecting applications via custom API actions.

The backend code is organized into `models`, `routes`, and `middleware` directories to maintain a clean and scalable structure.

### React Frontend

The frontend is a modern Single-Page Application built with React and Vite. Its responsibilities include:

-   **User Interface**: Rendering all user-facing pages, including the public volunteer signup form, the admin login page, and the main admin dashboard.
-   **Client-Side Routing**: Using `react-router-dom` to handle navigation between different pages without requiring a full page reload.
-   **State Management**: Using React hooks like `useState`, `useEffect`, and `useContext` to manage the application's state. This includes local component state (form inputs, etc.) and global application state like authentication status, which is managed in the `AuthContext`.
-   **API Communication**: Using the `axios` library to communicate with the Express backend's REST API. All API service functions are centralized in `frontend/src/services/api.js`. The `AuthContext` provider helps manage the user's authentication state, while a request interceptor in `api.js` automatically attaches the JWT to the headers of protected requests.

---

## Key Features in Detail

### Volunteer Application Lifecycle
The application manages the entire lifecycle of a volunteer application.

1.  **Public Signup**: A prospective volunteer fills out the public signup form. A new `Volunteer` record is created in the database with a `status` of `pending`.
2.  **Admin Review**: An authenticated administrator reviews the pending applications on the dashboard.
3.  **Approval/Rejection**: An admin can approve or reject an application. This simply updates the `status` field on the volunteer's record in the database.
4.  **Updates**: If an admin edits the details of a volunteer, the changes are saved to their record in the database.
5.  **Deletions**: If an admin deletes a volunteer, their record is removed from the database.

### CSV Bulk Import
To accommodate large-scale data entry, the application supports bulk importing of volunteers from a CSV file.

-   **Direct Approval**: Volunteers imported via CSV are considered pre-approved and are created in the local database with a status of `approved`.
-   **Batch Creation**: The backend parses the CSV file and uses a single efficient `insertMany` operation to add all volunteers to the database.

### Data Visualization
To provide administrators with at-a-glance insights into their volunteer community, a data visualization feature has been implemented.

-   **Backend Endpoint**: A dedicated API endpoint, `/api/visualizations/volunteer-roles`, aggregates `Volunteer` data from the database. It uses the MongoDB aggregation pipeline to group volunteers by their `preferred_volunteer_role` and returns a count for each role.
-   **Frontend Chart**: A "Visualizations" page in the admin section (`/admin/visualizations`) fetches data from this endpoint and renders it as a bar chart using the **Chart.js** library. This provides a clear and immediate view of which volunteer roles are most popular.
