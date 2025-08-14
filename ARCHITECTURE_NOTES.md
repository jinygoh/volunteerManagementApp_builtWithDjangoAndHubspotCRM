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

-   **Data Persistence**: It uses a local database (currently SQLite for development) to store all volunteer applications. The `volunteer.models.Volunteer` model is the core of the data structure, holding all volunteer information as well as their application `status` (`pending`, `approved`, `rejected`) and their `hubspot_id` once they are synced.
-   **Business Logic**: It contains the core business logic for the volunteer approval workflow. New signups are saved with a `pending` status. Only when an administrator approves them is the data sent to HubSpot.
-   **Serving a REST API**: It exposes a RESTful API built with **Django REST Framework (DRF)**. This API allows the frontend to perform all necessary actions, including:
    -   Publicly creating new volunteer applications.
    -   Authenticating administrators.
    -   Performing CRUD (Create, Read, Update, Delete) operations on volunteer records.
    -   Approving and rejecting applications via custom API actions.
-   **Third-Party Integration**: It manages the integration with the HubSpot API via the `volunteer.hubspot_api.HubspotAPI` service class. This service is only called after a volunteer is approved by an admin.

### React Frontend

The frontend is a modern Single-Page Application built with React and Vite. Its responsibilities include:

-   **User Interface**: Rendering all user-facing pages, including the public volunteer signup form, the admin login page, and the main admin dashboard.
-   **Client-Side Routing**: Using `react-router-dom` to handle navigation between different pages without requiring a full page reload.
-   **State Management**: Using React hooks like `useState` and `useEffect` to manage the application's state, such as form inputs and the list of volunteers fetched from the API.
-   **API Communication**: Using the `axios` library to communicate with the Django backend's REST API. All data is fetched and submitted via asynchronous API calls, which are centralized in the `frontend/src/services/api.js` module.

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
