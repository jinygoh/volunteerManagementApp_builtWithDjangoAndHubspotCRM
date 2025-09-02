# How to Run Tests for This Project

This guide provides a comprehensive overview of the testing suites that have been set up for this project and includes detailed instructions on how to run each type of test.

## 1. Backend Testing (Django)

The Django backend is equipped with a suite of unit and integration tests. These tests validate the models, API views, and business logic.

### What's Included
- **Test Files:** All backend tests are located in `hopehands/volunteer/tests.py`.
- **Test Database:** The test suite is configured to run against a separate, in-memory SQLite database. This makes the tests fast and ensures they do not interfere with your development database.

### How to Run the Tests
To run the complete backend test suite, navigate to the project's root directory and execute the following command:

```bash
python hopehands/manage.py test volunteer
```

## 2. Frontend Unit Testing (React)

The React frontend has a unit testing environment set up using [Vitest](https://vitest.dev/) and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/). This allows for testing individual React components in isolation.

### What's Included
- **Testing Framework:** Vitest is used as the test runner.
- **Example Test:** A sample test for the `LoginPage` component can be found at `frontend/src/pages/LoginPage.test.jsx`. This serves as a template for writing new tests.
- **Configuration:** The testing environment is configured in `frontend/vite.config.js`. It has been set up to ignore End-to-End test files.

### How to Run the Tests
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Run the test command:
    ```bash
    npm test
    ```

## 3. End-to-End (E2E) Integration Testing

E2E tests are designed to test the entire application flow from the user's perspective. These tests use [Playwright](https://playwright.dev/) to automate a real web browser and interact with the application just like a user would.

### Prerequisites
- **A Running Application:** E2E tests run against the live, running application. This means you must have **both the backend and frontend servers running**.
- **Database Setup:** The backend server needs to be connected to a database. You must have a MySQL server running and have your database credentials configured in a `.env` file in the project root (use `.env.example` as a template).

### What's Included
- **Test Framework:** Playwright is used to write and run the E2E tests.
- **Configuration:** The Playwright configuration is in `frontend/playwright.config.js`. It is set up to automatically start the frontend server.
- **Example Test:** A sample test that simulates a user signing up through the volunteer form is located at `frontend/tests/signup.spec.js`.

### How to Run the Tests
1.  **Start the Backend Server:**
    In a terminal, from the project root, start the Django server:
    ```bash
    python hopehands/manage.py runserver
    ```

2.  **Run the Playwright Tests:**
    In a **separate terminal**, navigate to the frontend directory and run the tests:
    ```bash
    cd frontend
    npx playwright test
    ```
    Playwright will automatically start the frontend development server and run the tests in a headless browser.

## 4. Performance Testing (Locust)

Performance testing is used to see how the backend API behaves under heavy load. This project uses [Locust](https://locust.io/) to simulate a large number of users accessing the API concurrently.

### Prerequisites
- **A Running Backend Server:** Like the E2E tests, the performance tests require a running backend server connected to a database.

### What's Included
- **Test Framework:** Locust is used for load testing.
- **Test Script:** The test script is located at `locustfile.py` in the project root. It simulates users submitting the volunteer signup form.

### How to Run the Tests
1.  **Start the Backend Server:**
    In a terminal, from the project root, start the Django server. It is recommended to use the `--noreload` flag to prevent the server from restarting during the test.
    ```bash
    python hopehands/manage.py runserver --noreload
    ```

2.  **Run Locust:**
    In a **separate terminal**, from the project root, start the Locust test. You can run it in headless mode for a quick test from the command line.

    **Example (Headless Mode):**
    This command will simulate 10 users for 20 seconds.
    ```bash
    locust -f locustfile.py --headless -u 10 -t 20s
    ```

    **Example (Web UI Mode):**
    To use Locust's more powerful web interface, simply run:
    ```bash
    locust
    ```
    Then open your web browser to `http://localhost:8089` to start the test and see real-time results.
