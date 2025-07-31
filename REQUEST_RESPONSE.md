# Request-Response Cycle: Volunteer Signup

This document describes the request-response cycle for the volunteer signup process in the HopeHands application.

The primary flow involves a user signing up as a volunteer and their data being saved to the database and sent to HubSpot.

## Cycle Breakdown

1.  **Initial Request (GET):**
    *   **Client (Browser):** A user navigates to the root URL (`/`) or `/volunteer/signup/`.
    *   **Server (Django):**
        *   The request is routed by `hopehands/urls.py` and `hopehands/volunteer/urls.py` to the `volunteer_signup` view function in `hopehands/volunteer/views.py`.
        *   Since the request method is `GET`, the view creates an instance of the `VolunteerForm`.
        *   The view then renders the `volunteer/signup.html` template, passing the empty form to it.
    *   **Response:** The server sends the rendered HTML page back to the client, displaying the volunteer signup form.

2.  **Form Submission (POST):**
    *   **Client (Browser):** The user fills out the form and clicks the "Submit" button. This sends a `POST` request to the same URL (`/volunteer/signup/`). The form data is included in the request body.
    *   **Server (Django):**
        *   The `volunteer_signup` view is called again.
        *   This time, the request method is `POST`. The view creates an instance of the `VolunteerForm`, populating it with the submitted data from `request.POST`.
        *   The view calls `form.is_valid()` to perform data validation.
        *   **If the form is valid:**
            1.  `form.save()` creates a new `Volunteer` object and saves it to the MySQL database.
            2.  The application prepares the volunteer's data (name, email, phone, etc.) to be sent to HubSpot.
            3.  It initializes the HubSpot API client using the `HUBSPOT_PRIVATE_APP_TOKEN` from the settings.
            4.  A new contact is created in HubSpot with the volunteer's details.
            5.  The view then redirects the user to the `/volunteer/success/` URL.
        *   **If the form is invalid:**
            1.  The view re-renders the `volunteer/signup.html` template.
            2.  The form instance, now containing the submitted data and any validation errors, is passed to the template.
            3.  The template displays the form with the user's previously entered data and shows the validation errors.

3.  **Success Page (GET):**
    *   **Client (Browser):** After the redirect, the browser sends a `GET` request to `/volunteer/success/`.
    *   **Server (Django):**
        *   The request is routed to the `success` view in `hopehands/volunteer/views.py`.
        *   The view renders the `volunteer/success.html` template.
    *   **Response:** The server sends the rendered success page to the client, confirming that the signup was successful.

## Visual Flow

```
+----------+           +-----------------+           +-----------------+
|          | --GET-->  |                 |           |                 |
|  Client  |           |  Django Server  | --------> |     MySQL DB    |
|          | <--HTML-- | (views.py)      |           | (Save Volunteer)|
+----------+           |                 |           |                 |
     |                 +-----------------+           +-----------------+
     |                       ^     |
     | POST (Form Data)      |     | (API Call)
     |                       |     v
     |                 +-----------------+
     |                 |                 |
     +---------------->|  HubSpot API    |
                       | (Create Contact)|
                       |                 |
                       +-----------------+
```
