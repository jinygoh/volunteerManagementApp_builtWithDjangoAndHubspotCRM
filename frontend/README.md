# HopeHands Frontend

This directory contains the React single-page application (SPA) for the HopeHands Volunteer Management system. It provides the user interface for both public volunteer signups and the administrator's dashboard for managing applications.

## Tech Stack

-   **Framework**: React
-   **Build Tool**: Vite
-   **Routing**: React Router
-   **Styling**: Bootstrap 5 & custom CSS (`src/assets/style.css`)
-   **API Communication**: Axios

## Project Structure

The source code is located in the `src/` directory and is organized as follows:

-   **`src/components/`**: Contains reusable components that are used across multiple pages (e.g., `ProtectedRoute`).
-   **`src/context/`**: Contains React Context providers, such as the `AuthContext` which manages global authentication state.
-   **`src/pages/`**: Contains the top-level component for each "page" of the application (e.g., `DashboardPage`, `LoginPage`).
-   **`src/services/`**: Contains modules that handle external interactions. `api.js` centralizes all HTTP requests to the backend.
-   **`src/App.jsx`**: The main application component that sets up routing.
-   **`src/main.jsx`**: The entry point of the application.

## Getting Started

### Prerequisites

-   Node.js and npm (or yarn/pnpm) must be installed.
-   The Django backend server must be running.

### Installation

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the required Node.js packages:
    ```bash
    npm install
    ```

### Running the Development Server

To start the Vite development server, run:
```bash
npm run dev
```
The application will be available at `http://127.0.0.1:5173` (or the next available port). The Vite server is configured with a proxy, so any requests made to `/api` will be automatically forwarded to the Django backend running on `http://127.0.0.1:8000`.
