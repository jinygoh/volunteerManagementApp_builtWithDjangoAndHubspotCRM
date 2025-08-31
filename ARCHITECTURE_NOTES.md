# Architecture Notes

This document contains notes and explanations about key architectural and design decisions in the HopeHands Volunteer Management application.

---

## High-Level Architecture

The application is designed as a modern, decoupled web application with two main parts:

1.  **A Django REST API Backend**: Serves as the data and logic layer.
2.  **A React Single-Page Application (SPA) Frontend**: Provides the user interface.

This separation of concerns allows for independent development, testing, and deployment of the backend and frontend.

### Django Backend

The backend is built with the Django web framework and is responsible for:

-   **Data Persistence**: It uses a MySQL database to store all volunteer applications, configured via environment variables. The `volunteer.models.Volunteer` model is the core of the data structure, holding all volunteer information as well as their application `status` (`pending`, `approved`, `rejected`) and their `hubspot_id` once they are synced.
-   **Business Logic**: It contains the core business logic for the volunteer approval workflow and data synchronization with HubSpot.
-   **Serving a REST API**: It exposes a RESTful API built with **Django REST Framework (DRF)**. This API allows the frontend to perform all necessary actions, including:
    -   Publicly creating new volunteer applications.
    -   Authenticating administrators.
    -   Performing CRUD (Create, Read, Update, Delete) operations on volunteer records.
    -   Approving and rejecting applications via custom API actions.
-   **Third-Party Integration**: It manages the integration with the HubSpot API via the `volunteer.hubspot_api.HubspotAPI` service class. This service handles the synchronization of volunteer data (creation, updates, and deletion) with HubSpot contacts.

### React Frontend

The frontend is a modern Single-Page Application built with React and Vite. Its responsibilities include:

-   **User Interface**: Rendering all user-facing pages, including the public volunteer signup form, the admin login page, and the main admin dashboard.
-   **Client-Side Routing**: Using `react-router-dom` to handle navigation between different pages without requiring a full page reload.
-   **State Management**: Using React hooks like `useState`, `useEffect`, and `useContext` to manage the application's state. This includes local component state (form inputs, etc.) and global application state like authentication status, which is managed in the `AuthContext`.
-   **API Communication**: Using the `axios` library to communicate with the Django backend's REST API. All API service functions are centralized in `frontend/src/services/api.js`. The `AuthContext` provider configures Axios interceptors to automatically handle JWT token attachment to headers and to refresh expired tokens, centralizing authentication logic.

---

## The Role of `manage.py` and `load_dotenv()`

A question was raised about why `load_dotenv()` is called in `manage.py` instead of another place like `settings.py`. This is an excellent question that gets to the heart of how Django projects are loaded and configured.

### The Problem: When Do Environment Variables Need to be Loaded?

The Django application relies on environment variables (like `HUBSPOT_PRIVATE_APP_TOKEN`, `DB_NAME`, etc.) that are defined in a `.env` file. These variables are crucial for the application to function correctly, as they contain sensitive information and configuration details that can change between different environments (e.g., development, testing, production).

These variables need to be loaded into the environment *before* Django starts to configure itself. Specifically, they must be available before Django reads the `settings.py` file, because `settings.py` is where those variables are actually read and used to configure the database, API clients, and other parts of the application.

### Why `manage.py` is the Correct Entry Point

The `manage.py` script is the primary entry point for almost all interactions with a Django project. Whenever you run a command from your terminal, you are starting with this script:

-   `python manage.py runserver` (to start the development server)
-   `python manage.py migrate` (to apply database migrations)
-   `python manage.py shell` (to open an interactive shell)
-   `python manage.py test` (to run tests)

By placing the `load_dotenv()` function at the top of `manage.py`, we ensure that the environment variables from the `.env` file are loaded into the system's environment right at the beginning. This happens *before* any of Django's own machinery kicks in and starts looking for the settings.

### What if `load_dotenv()` was in `settings.py`?

If you were to put `load_dotenv()` inside `settings.py`, you might run into a "chicken and egg" problem. The settings file itself is the one trying to access the environment variables, so it needs them to be loaded *before* it runs. While putting `load_dotenv()` at the very top of `settings.py` can sometimes work for simple cases like `runserver`, it is not as robust. Other management commands or tools might import the settings in a way that causes issues.

Placing `load_dotenv()` in `manage.py` guarantees that for any standard management command, the environment is correctly and reliably set up before anything else happens.

### The `main()` function in `manage.py`

Let's examine the structure of `manage.py` to see this in action:

```python
# hopehands/manage.py

import os
import sys
from dotenv import load_dotenv # Assuming dotenv is used

def main():
    """Run administrative tasks."""
    # This is where we load the .env file. It's the first thing we do.
    load_dotenv()

    # Now that the environment is set, we can safely tell Django where to find its settings.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hopehands.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # This function runs the Django command, and by now, the settings are available.
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
```

As you can see, `load_dotenv()` is the very first operational call inside the `main()` function. This ensures that when `execute_from_command_line(sys.argv)` is called—which is the function that actually runs the Django command you specified (like `runserver` or `migrate`)—the environment is already fully configured with the variables from your `.env` file.

In summary, placing `load_dotenv()` in `manage.py` is a strategic choice to ensure that the application's environment is set up correctly and reliably at the earliest possible moment, making the settings available to the entire Django application for any management command you run.

---

## Key Features in Detail

### Data Sync Lifecycle with HubSpot
The application maintains a synchronized relationship with HubSpot, ensuring that the CRM is always up-to-date with the status of approved volunteers.

1.  **Public Signup**: A prospective volunteer fills out the public signup form. A new `Volunteer` record is created in the local database with a `status` of `pending`. No data is sent to HubSpot at this stage.
2.  **Admin Review**: An authenticated administrator reviews the pending applications on the dashboard.
3.  **Approval and Creation**: When an admin approves an application, the volunteer's status is changed to `approved`, and their information is synced to HubSpot, creating a new contact. The unique HubSpot ID is then saved back to the local `Volunteer` record.
4.  **Rejection**: If an application is rejected, the status is simply updated to `rejected`, and no data is sent to HubSpot.
5.  **Updates**: If an admin edits the details of an *approved* volunteer, the changes are synced to HubSpot, updating the corresponding contact's properties.
6.  **Deletions**: If an admin deletes a volunteer who has been previously synced to HubSpot, the application makes a corresponding API call to **archive** the contact in HubSpot, keeping the two systems in sync.

### CSV Bulk Import
To accommodate large-scale data entry, the application supports bulk importing of volunteers from a CSV file. This feature is designed for efficiency and immediate synchronization.

-   **Direct Approval**: Volunteers imported via CSV are considered pre-approved and are created in the local database with a status of `approved`.
-   **Batch Synchronization**: Immediately after the local records are created, their information is sent to HubSpot using a single, efficient **batch API request** (`hubspot_api.batch_create_contacts`). This minimizes the number of API calls.
-   **ID-Linking**: The system processes the response from the batch API call, extracts the new HubSpot IDs, and updates the corresponding local volunteer records.

### Data Visualization
To provide administrators with at-a-glance insights into their volunteer community, a data visualization feature has been implemented.

-   **Backend Endpoint**: A dedicated API endpoint, `/api/visualizations/volunteer-roles/`, aggregates `Volunteer` data from the database. It groups volunteers by their `preferred_volunteer_role` and returns a count for each role.
-   **Frontend Chart**: A new "Visualizations" page in the admin section (`/admin/visualizations`) fetches data from this endpoint and renders it as a bar chart using the **Chart.js** library. This provides a clear and immediate view of which volunteer roles are most popular.
