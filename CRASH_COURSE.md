# HopeHands Volunteer Management App - Crash Course

Welcome to the HopeHands Volunteer Management App! This document provides a crash course on the project's architecture, setup, and key functionalities.

## 1. Project Overview

This is a Django application designed to manage volunteers for the HopeHands organization. The core feature is the integration with HubSpot CRM, which is used as the primary data store for all volunteer information. The application provides a web interface for performing CRUD (Create, Read, Update, Delete) operations on volunteers and for batch uploading volunteers from a CSV file.

## 2. Architecture

The application follows a standard Django architecture, with some key components:

- **Project Directory (`hopehands/`):** This is the main project directory, which contains the project-level settings and URL configuration.
- **App Directory (`hopehands/volunteer/`):** This is the main application directory, which contains the models, views, forms, templates, and other application-specific code.
- **HubSpot API Service (`hopehands/volunteer/hubspot_api.py`):** This is a dedicated service that encapsulates all interactions with the HubSpot API. This keeps the views clean and makes the HubSpot integration easy to manage.
- **Templates (`hopehands/volunteer/templates/`):** The HTML templates for the application, which are rendered by the views.
- **Static Files (`hopehands/volunteer/static/`):** The CSS, JavaScript, and other static files for the application.

## 3. Setup and Installation

To run this application locally, you will need to have Python, pip, and MySQL installed.

### a. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### b. Set Up the Environment
The application uses a `.env` file to manage environment variables. Create a `.env` file in the root of the project with the following content:

```
DJANGO_SECRET_KEY="your-django-secret-key"
DJANGO_DEBUG="True"
DB_NAME="hopehands"
DB_USER="user"
DB_PASSWORD="password"
HUBSPOT_PRIVATE_APP_TOKEN="your-hubspot-private-app-token"
```
- **`DJANGO_SECRET_KEY`**: A secret key for a particular Django installation.
- **`DJANGO_DEBUG`**: Set to `True` for development, `False` for production.
- **`DB_NAME`**, **`DB_USER`**, **`DB_PASSWORD`**: Your MySQL database credentials.
- **`HUBSPOT_PRIVATE_APP_TOKEN`**: Your private app token from HubSpot.

### c. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
If you encounter issues with `mysqlclient`, you may need to install the MySQL development libraries for your system. On Debian-based systems:
```bash
sudo apt-get install libmysqlclient-dev
```

### d. Set Up the Database
You will need to have a MySQL server running. Once it's running, you need to create the database and user that you specified in your `.env` file. You can do this from the MySQL command line:
```sql
CREATE DATABASE hopehands;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON hopehands.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

### e. Run Database Migrations
Apply the database migrations to create the necessary tables:
```bash
python hopehands/manage.py migrate
```

### f. Run the Development Server
Start the Django development server:
```bash
python hopehands/manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## 4. Key Functionalities and Code References

### a. Volunteer Signup (Create)
- **URL:** `/` or `/volunteer/signup/`
- **View:** `volunteer_signup` in `hopehands/volunteer/views.py`
- **Form:** `VolunteerForm` in `hopehands/volunteer/forms.py`
- **Template:** `hopehands/volunteer/templates/volunteer/signup.html`
- **HubSpot API Method:** `create_contact` in `hopehands/volunteer/hubspot_api.py`

This feature allows a new volunteer to sign up through a web form. The data is saved to the local database and then sent to HubSpot.

### b. Volunteer List (Read)
- **URL:** `/volunteer/list/`
- **View:** `volunteer_list` in `hopehands/volunteer/views.py`
- **Template:** `hopehands/volunteer/templates/volunteer/volunteer_list.html`
- **HubSpot API Method:** `get_all_contacts` in `hopehands/volunteer/hubspot_api.py`

This page displays a list of all volunteers fetched from HubSpot.

### c. Volunteer Detail (Read)
- **URL:** `/volunteer/contact/<int:contact_id>/`
- **View:** `volunteer_detail` in `hopehands/volunteer/views.py`
- **Template:** `hopehands/volunteer/templates/volunteer/volunteer_detail.html`
- **HubSpot API Method:** `get_contact` in `hopehands/volunteer/hubspot_api.py`

This page shows the details of a single volunteer.

### d. Volunteer Update
- **URL:** `/volunteer/contact/<int:contact_id>/update/`
- **View:** `volunteer_update` in `hopehands/volunteer/views.py`
- **Form:** `VolunteerForm` in `hopehands/volunteer/forms.py`
- **Template:** `hopehands/volunteer/templates/volunteer/volunteer_update.html`
- **HubSpot API Method:** `update_contact` in `hopehands/volunteer/hubspot_api.py`

This feature allows for editing the details of an existing volunteer.

### e. Volunteer Delete
- **URL:** `/volunteer/contact/<int:contact_id>/delete/`
- **View:** `volunteer_delete` in `hopehands/volunteer/views.py`
- **Template:** `hopehands/volunteer/templates/volunteer/volunteer_delete_confirm.html`
- **HubSpot API Method:** `delete_contact` in `hopehands/volunteer/hubspot_api.py`

This feature allows for deleting a volunteer from HubSpot and the local database.

### f. Batch CSV Upload
- **URL:** `/volunteer/upload-csv/`
- **View:** `volunteer_csv_upload` in `hopehands/volunteer/views.py`
- **Form:** `CSVUploadForm` in `hopehands/volunteer/forms.py`
- **Template:** `hopehands/volunteer/templates/volunteer/volunteer_csv_upload.html`
- **HubSpot API Method:** `batch_create_contacts` in `hopehands/volunteer/hubspot_api.py`

This feature allows for uploading a CSV file of volunteers to be created in HubSpot in a single batch operation.

---
This crash course should provide a good starting point for understanding and working with the HopeHands Volunteer Management App. For more detailed information, please refer to the code comments and the official Django and HubSpot API documentation.
