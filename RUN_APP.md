# How to Set Up and Run the Volunteer Management Application

This document outlines the steps to set up and run the Volunteer Management Application, which consists of a Django backend and a React frontend.

## Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   Node.js (LTS version recommended)
*   npm (Node Package Manager, comes with Node.js)

## Setup Steps

shortcut copy paste for backend

py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cd hopehands
python manage.py makemigrations
python manage.py migrate
py manage.py runserver

shortcut copy paste for front end

cd frontend
npm install
npm run dev

### 1. Backend Setup (Django)

1.  **Navigate to the backend directory:**
    ```bash
    cd hopehands
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` in the root directory of the project (not inside `hopehands` or `frontend`).
    ```bash
    cp ../.env.example ./.env
    ```
    Open the newly created `.env` file and fill in the necessary environment variables, such as `HUBSPOT_PRIVATE_APP_TOKEN`, database credentials, etc. (Refer to the `.env.example` for required variables).

### 2. Frontend Setup (React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

## Running the Application

To run the complete application, you need to start both the backend and the frontend servers. It is recommended to open two separate terminal windows for this.

### 1. Start the Backend Server

In the terminal window where you performed the backend setup (you should be in the `hopehands` directory):

```bash
python manage.py runserver
```
This will typically start the Django development server at `http://127.0.0.1:8000/`.

### 2. Start the Frontend Server

In a **new** terminal window, navigate to the `frontend` directory:

```bash
cd frontend
npm start
or
npm run dev
```
This will typically start the React development server at `http://localhost:3000/` and open the application in your web browser.

You should now be able to access the application in your web browser at `http://localhost:3000/`.
