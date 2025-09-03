# How to Set Up and Run the Volunteer Management Application

This document outlines the steps to set up and run the Volunteer Management Application, which consists of a Spring Boot backend and a React frontend.

## Prerequisites

*   Java 17 or later
*   Maven
*   Node.js (LTS version recommended)
*   npm (Node Package Manager, comes with Node.js)

## Setup Steps

### 1. Backend Setup (Spring Boot)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` in the root directory of the project.
    ```bash
    cp ../.env.example ./.env
    ```
    Open the newly created `.env` file and fill in the necessary environment variables for the database.

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

In the terminal window where you performed the backend setup (you should be in the `backend` directory):

```bash
mvn spring-boot:run
```
This will typically start the Spring Boot development server at `http://127.0.0.1:8080/`.

### 2. Start the Frontend Server

In a **new** terminal window, navigate to the `frontend` directory:

```bash
cd frontend
npm run dev
```
This will typically start the Vite development server at `http://localhost:5173/` and open the application in your web browser.

You should now be able to access the application in your web browser at `http://localhost:5173/`.

---

## Running Tests

### Backend Tests

The project includes a test suite for the Spring Boot backend. To run these tests, navigate to the `backend` directory and run the following command:

```bash
mvn test
```

### Frontend Tests

There are currently no automated tests configured for the React frontend.
