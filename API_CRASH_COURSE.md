# REST API Crash Course

This guide explains how to use the REST API for the HopeHands Volunteer Management application. The API is the interface between the frontend and the backend.

## 1. API Root

The root of the API is available at:

`/api/`

All endpoints are relative to this URL. For example, the volunteers endpoint is at `/api/volunteers/`.

## 2. Authentication

Most API endpoints are protected and require authentication.

-   **How to Authenticate**: To log in, send a `POST` request to `/api/token/` with a JSON body containing your `username` and `password`. If successful, the API will return `access` and `refresh` JSON Web Tokens (JWT). All subsequent requests to protected API endpoints must include the access token in the `Authorization` header, formatted as `Bearer <your_access_token>`.
-   **Public Endpoints**: The only public endpoint that does not require authentication is `/api/signup/`. The token endpoints (`/api/token/` and `/api/token/refresh/`) are also public.

---

## 3. Key Endpoints

Here are the main endpoints and how to use them.

### **Volunteer Signup**

-   **Endpoint**: `POST /api/signup/`
-   **Authentication**: None required.
-   **Description**: Creates a new volunteer application. The new volunteer will have a `status` of `pending`.
-   **Request Body (JSON)**:
    ```json
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "555-123-4567",
        "preferred_volunteer_role": "Event Staff",
        "availability": "Saturday Mornings",
        "how_did_you_hear_about_us": "A friend"
    }
    ```
-   **Success Response**: `201 Created` with the full volunteer object in the body.

---

### **List and Manage Volunteers (Admin)**

This set of endpoints is managed by a `ModelViewSet` and requires authentication.

#### List All Volunteers

-   **Endpoint**: `GET /api/volunteers/`
-   **Authentication**: Required.
-   **Description**: Retrieves a list of all volunteer applications in the system.
-   **Success Response**: `200 OK` with a JSON list of volunteer objects in the body.
    ```json
    [
        {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "status": "pending",
            ...
        },
        ...
    ]
    ```

#### Retrieve a Single Volunteer

-   **Endpoint**: `GET /api/volunteers/{id}/`
-   **Authentication**: Required.
-   **Description**: Retrieves the details for a single volunteer.
-   **Success Response**: `200 OK` with the volunteer object in the body.

#### Update a Volunteer

-   **Endpoint**: `PUT /api/volunteers/{id}/` or `PATCH /api/volunteers/{id}/`
-   **Authentication**: Required.
-   **Description**: Updates the details for a volunteer. `PUT` requires all fields, while `PATCH` allows for partial updates.
-   **Request Body (JSON)**:
    ```json
    {
        "phone_number": "555-765-4321"
    }
    ```
-   **Success Response**: `200 OK` with the updated volunteer object.

---

### **Approval Workflow Endpoints (Admin)**

These are custom actions on the volunteer endpoint.

#### Approve a Volunteer

-   **Endpoint**: `POST /api/volunteers/{id}/approve/`
-   **Authentication**: Required.
-   **Description**: Approves a pending volunteer application. This will change their `status` to `approved` and trigger the synchronization with HubSpot.
-   **Request Body**: None required.
-   **Success Response**: `200 OK` with a status message.
    ```json
    {
        "status": "volunteer approved"
    }
    ```

#### Reject a Volunteer

-   **Endpoint**: `POST /api/volunteers/{id}/reject/`
-   **Authentication**: Required.
-   **Description**: Rejects a pending volunteer application. This will change their `status` to `rejected`.
-   **Request Body**: None required.
-   **Success Response**: `200 OK` with a status message.
    ```json
    {
        "status": "volunteer rejected"
    }
    ```
This guide covers the essential API endpoints for interacting with the HopeHands application.
