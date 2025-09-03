# HopeHands Volunteer Management App - Crash Course

Welcome to the HopeHands Volunteer Management App! This document provides a crash course on the project's architecture, setup, and key functionalities.

## 1. Project Overview

This is a full-stack application designed to manage volunteers for the HopeHands organization. It features a modern, decoupled architecture:

-   **Spring Boot REST API Backend**: A robust backend that handles all business logic and data storage.
-   **React Single-Page Application (SPA) Frontend**: A dynamic and responsive user interface for both volunteers and administrators.

The core workflow involves volunteers signing up and their applications being stored locally for admin review.

## 2. Architecture

For a detailed explanation of the architecture, please see [ARCHITECTURE_NOTES.md](./ARCHITECTURE_NOTES.md).

For a guide on how to read the code and trace feature flows, see [CODE_READING_GUIDE.md](./CODE_READING_GUIDE.md).

## 3. Setup and Installation

To run this application locally, you will need to have Java, Maven, and Node.js/npm installed.

### a. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### b. Set Up the Backend Environment
The backend uses a `.env` file to manage environment variables for the database. Create a `.env` file in the project root with the following content:

```
DB_NAME="your_db_name"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
```

### c. Set Up the Frontend Environment
Navigate to the frontend directory and install the required Node.js packages:
```bash
cd frontend
npm install
cd ..
```

### d. Set Up the Database
The application is configured to use a MySQL database. Ensure you have a running MySQL server. The Spring Boot application will automatically create the database schema based on the entities.

### e. Create an Admin User
To log in to the admin dashboard, you'll need a superuser account. The application is configured to create a default admin user on startup. You can modify the `DataInitializer` class to change the default credentials.

### f. Run the Development Servers
For the application to work, you need to run both the backend and frontend development servers simultaneously. Open two separate terminal windows.

**In Terminal 1 (Backend):**
```bash
cd backend
mvn spring-boot:run
```
The Spring Boot API will be running at `http://127.0.0.1:8080`.

**In Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
The React application will be available at `http://127.0.0.1:5173` (or another port if 5173 is in use). You should open this URL in your browser.

## 4. Crash Courses for Different Parts of the App

To learn more about the specifics of the implementation, please refer to the following guides:

-   **[Spring Boot Backend Crash Course](./SPRING_BOOT_CRASH_COURSE.md)**: An introduction to the Spring Boot models, repositories, services, and controllers.
-   **[REST API Crash Course](./API_CRASH_COURSE.md)**: A guide to understanding and using the backend REST API.
-   **[React Frontend Crash Course](./REACT_CRASH_COURSE.md)**: An introduction to the React components, services, and state management.
