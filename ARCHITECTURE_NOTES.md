# Architecture Notes

This document contains notes and explanations about key architectural and design decisions in the HopeHands Volunteer Management application.

---

## High-Level Architecture

The application is designed as a modern, decoupled web application with two main parts:

1.  **A Spring Boot REST API Backend**: Serves as the data and logic layer.
2.  **A React Single-Page Application (SPA) Frontend**: Provides the user interface.

This separation of concerns allows for independent development, testing, and deployment of the backend and frontend.

### Spring Boot Backend

The backend is built with the Spring Boot framework and is responsible for:

-   **Data Persistence**: It uses a MySQL database to store all volunteer applications, configured via environment variables. The `com.hopehands.model.Volunteer` entity is the core of the data structure, holding all volunteer information as well as their application `status` (`pending`, `approved`, `rejected`).
-   **Business Logic**: It contains the core business logic for the volunteer approval workflow.
-   **Serving a REST API**: It exposes a RESTful API. This API allows the frontend to perform all necessary actions, including:
    -   Publicly creating new volunteer applications.
    -   Authenticating administrators.
    -   Performing CRUD (Create, Read, Update, Delete) operations on volunteer records.
    -   Approving and rejecting applications via custom API actions.

### React Frontend

The frontend is a modern Single-Page Application built with React and Vite. Its responsibilities include:

-   **User Interface**: Rendering all user-facing pages, including the public volunteer signup form, the admin login page, and the main admin dashboard.
-   **Client-Side Routing**: Using `react-router-dom` to handle navigation between different pages without requiring a full page reload.
-   **State Management**: Using React hooks like `useState`, `useEffect`, and `useContext` to manage the application's state. This includes local component state (form inputs, etc.) and global application state like authentication status, which is managed in the `AuthContext`.
-   **API Communication**: Using the `axios` library to communicate with the Spring Boot backend's REST API. All API service functions are centralized in `frontend/src/services/api.js`. The `AuthContext` provider configures Axios interceptors to automatically handle JWT token attachment to headers and to refresh expired tokens, centralizing authentication logic.

---

## Environment Variables in Spring Boot

The Spring Boot application relies on environment variables (like `DB_NAME`, etc.) that can be defined in a `.env` file and loaded by the operating system, or passed as command-line arguments. These variables are crucial for the application to function correctly.

Spring Boot automatically reads environment variables and properties from `application.properties`. We can use placeholders in `application.properties` to refer to environment variables.

For example, in `application.properties`:
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/${DB_NAME}
```
Spring will replace `${DB_NAME}` with the value of the `DB_NAME` environment variable.

---

## Key Features in Detail

### CSV Bulk Import
To accommodate large-scale data entry, the application supports bulk importing of volunteers from a CSV file.

-   **Direct Approval**: Volunteers imported via CSV are considered pre-approved and are created in the local database with a status of `approved`.

### Data Visualization
To provide administrators with at-a-glance insights into their volunteer community, a data visualization feature has been implemented.

-   **Backend Endpoint**: A dedicated API endpoint, `/api/visualizations/volunteer-roles/`, aggregates `Volunteer` data from the database. It groups volunteers by their `preferred_volunteer_role` and returns a count for each role.
-   **Frontend Chart**: A new "Visualizations" page in the admin section (`/admin/visualizations`) fetches data from this endpoint and renders it as a bar chart using the **Chart.js** library. This provides a clear and immediate view of which volunteer roles are most popular.
