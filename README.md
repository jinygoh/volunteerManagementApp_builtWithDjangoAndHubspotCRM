# HopeHands Volunteer Management

This is a volunteer management web application for the HopeHands charitable organization. It is built with Django and integrates with HubSpot to manage volunteer data.

## Features

*   Volunteer registration
*   CRUD operations for managing volunteers
*   Bulk import of volunteer information via CSV files
*   HubSpot integration to synchronize contact data
*   User authentication and authorization
*   Volunteer approval workflow
*   Visualization of volunteer data

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure the HubSpot API key:**
    *   Follow the instructions in `HUBSPOT_API_KEY_INSTRUCTIONS.md` to get your HubSpot API key.
    *   Open the `hopehands/settings.py` file and replace `'your-hubspot-api-key'` with your actual API key.
4.  **Run the migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

*   Access the application at `http://127.0.0.1:8000/`.
*   Log in with your superuser credentials to access the admin interface and manage volunteers.
*   Register new volunteers at `http://127.0.0.1:8000/crm/register/`.
*   View the list of volunteers at `http://127.0.0.1:8000/crm/`.
*   View the skills chart at `http://127.0.0.1:8000/crm/skills-chart/`.
*   View pending volunteers at `http://127.0.0.1:8000/crm/pending/`.
*   Import volunteers from a CSV file at `http://127.0.0.1:8000/crm/import/`.
