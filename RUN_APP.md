# How to Set Up and Run the Volunteer Management Application

This document outlines the steps to set up and run the Volunteer Management Application, which consists of an Express.js backend and a React frontend.

## Prerequisites

*   Node.js (LTS version recommended)
*   npm (Node Package Manager, comes with Node.js)
*   A running MongoDB instance (either local or on a cloud service like MongoDB Atlas)

## Setup Steps

### 1. Backend Setup (Express.js)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Create a `.env` file:**
    Inside the `backend` directory, copy the `backend/.env.example` file to a new file named `.env`.
    ```bash
    cp .env.example .env
    ```
    Open the newly created `.env` file and fill in the necessary environment variables:
    *   `MONGO_URI`: The connection string for your MongoDB database.
    *   `JWT_SECRET`: A long, random, secret string for signing authentication tokens.

### 2. Frontend Setup (React)

1.  **Navigate to the frontend directory:**
    From the project root, run:
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

In the terminal window where you performed the backend setup (you should be in the `backend` directory):

```bash
npm start
```
This will start the Express.js server, typically at `http://localhost:5000/`.

### 2. Start the Frontend Server

In a **new** terminal window, navigate to the `frontend` directory:

```bash
cd frontend
npm run dev
```
This will start the Vite development server, typically at `http://localhost:5173/`, and may open the application in your web browser.

You should now be able to access the application in your web browser. The frontend is configured to proxy API requests to the backend.

---

## Creating the First Admin User

The application does not have a public registration page for admin users. To create the first administrator, you must use a command-line tool like `curl` to send a request to the registration API endpoint **after** the backend server is running.

```bash
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "your_admin_username", "password": "your_strong_password"}'
```

After running this command, you can use these credentials to log in on the admin login page.

---

## Running Tests

There are currently no automated tests configured for the backend or the frontend.
