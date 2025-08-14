# HopeHands Volunteer Management App - Crash Course

Welcome to the HopeHands Volunteer Management App! This document provides a crash course on the project's architecture, setup, and key functionalities.

## 1. Project Overview

This is a full-stack application designed to manage volunteers for the HopeHands organization. It features a modern, decoupled architecture:

-   **Django REST API Backend**: A robust backend that handles all business logic, data storage, and integration with the HubSpot CRM.
-   **React Single-Page Application (SPA) Frontend**: A dynamic and responsive user interface for both volunteers and administrators.

The core workflow involves volunteers signing up, their applications being stored locally for admin review, and upon approval, their data being synced to HubSpot.

## 2. Architecture

For a detailed explanation of the architecture, please see [ARCHITECTURE_NOTES.md](./ARCHITECTURE_NOTES.md).

For a guide on how to read the code and trace feature flows, see [CODE_READING_GUIDE.md](./CODE_READING_GUIDE.md).

## 3. Setup and Installation

To run this application locally, you will need to have Python, pip, and Node.js/npm installed.

### a. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### b. Set Up the Backend Environment
The backend uses a `.env` file to manage environment variables. Create a `.env` file in the project root with the following content:

```
DJANGO_SECRET_KEY="your-django-secret-key"
DJANGO_DEBUG="True"
HUBSPOT_PRIVATE_APP_TOKEN="your-hubspot-private-app-token"
```
-   **`DJANGO_SECRET_KEY`**: A secret key for a particular Django installation. You can generate one easily.
-   **`DJANGO_DEBUG`**: Set to `True` for development.
-   **`HUBSPOT_PRIVATE_APP_TOKEN`**: Your private app token from HubSpot.

Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### c. Set Up the Frontend Environment
Navigate to the frontend directory and install the required Node.js packages:
```bash
cd frontend
npm install
cd ..
```

### d. Set Up the Database
The application is configured to use SQLite for local development, which requires no extra setup. The database file (`db.sqlite3`) will be created automatically. Simply run the migrations:
```bash
python hopehands/manage.py migrate
```

### e. Create an Admin User
To log in to the admin dashboard, you'll need a superuser account. Create one with this command and follow the prompts:
```bash
python hopehands/manage.py createsuperuser
```

### f. Run the Development Servers
For the application to work, you need to run both the backend and frontend development servers simultaneously. Open two separate terminal windows.

**In Terminal 1 (Backend):**
```bash
python hopehands/manage.py runserver
```
The Django API will be running at `http://127.0.0.1:8000`.

**In Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
The React application will be available at `http://127.0.0.1:5173` (or another port if 5173 is in use). You should open this URL in your browser.

## 4. Crash Courses for Different Parts of the App

To learn more about the specifics of the implementation, please refer to the following guides:

-   **[Django Backend Crash Course](./DJANGO_CRASH_COURSE.md)**: An introduction to the Django models, views, and business logic.
-   **[REST API Crash Course](./API_CRASH_COURSE.md)**: A guide to understanding and using the backend REST API.
-   **[React Frontend Crash Course](./REACT_CRASH_COURSE.md)**: An introduction to the React components, services, and state management.
