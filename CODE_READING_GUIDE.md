# How to Read the Code: A Guide to Understanding the Flow

This guide provides a step-by-step process for reading and understanding the code of the HopeHands Volunteer Management application. The separation of concerns (keeping different types of logic in different files) is a best practice that makes the code cleaner and more maintainable. This guide will help you navigate this structure.

## The Core Principle: Start at the URL, End at the UI

For any feature, the flow generally follows this path:

**URL -> View -> Service (API) -> Template (UI)**

Here's how to apply this principle to each of the CRUD (Create, Read, Update, Delete) operations.

---

### 1. Create (Volunteer Signup)

This is the flow for adding a new volunteer to the system.

1.  **Start at the "Map" - `urls.py`:**
    *   Open `hopehands/volunteer/urls.py`.
    *   Find the line: `path('signup/', views.volunteer_signup, name='signup')`.
    *   **Conclusion:** The `/signup/` URL is handled by the `volunteer_signup` function in `views.py`.

2.  **Follow the "Logic" - `views.py`:**
    *   Open `hopehands/volunteer/views.py` and find the `volunteer_signup` function.
    *   You'll see it handles two cases:
        *   **GET Request:** If it's a simple visit to the page, it just creates an empty `VolunteerForm` and renders the `signup.html` template.
        *   **POST Request:** If the user is submitting the form, it validates the data, saves it to the local database (`form.save()`), and then calls the HubSpot service: `hubspot_api.create_contact(...)`.

3.  **Jump to the "Service" - `hubspot_api.py`:**
    *   Open `hopehands/volunteer/hubspot_api.py` and find the `create_contact` method.
    *   **Conclusion:** This method takes the volunteer's data, formats it into the structure that the HubSpot API expects, and sends a POST request to create the contact in HubSpot.

4.  **End at the "User Interface" - `signup.html` & `success.html`:**
    *   The `volunteer_signup` view renders the `signup.html` template to display the form.
    *   After a successful submission, it redirects to the 'success' URL, which renders the `success.html` template.

---

### 2. Read (Volunteer List & Detail)

This is the flow for viewing the list of all volunteers and the details of a single volunteer.

#### a. Volunteer List (Read All)

1.  **URL (`urls.py`):** `path('list/', views.volunteer_list, name='volunteer_list')`
2.  **View (`views.py`):** In the `volunteer_list` function, you'll see a call to `hubspot_api.get_all_contacts()`.
3.  **Service (`hubspot_api.py`):** The `get_all_contacts` method sends a GET request to the HubSpot API to fetch all contacts.
4.  **UI (`volunteer_list.html`):** The view takes the list of contacts returned by the service and passes it to the `volunteer_list.html` template, which then loops through the list to display each volunteer in a table.

#### b. Volunteer Detail (Read One)

1.  **URL (`urls.py`):** `path('contact/<int:contact_id>/', views.volunteer_detail, name='volunteer_detail')`
2.  **View (`views.py`):** The `volunteer_detail` function takes the `contact_id` from the URL and calls `hubspot_api.get_contact(contact_id)`.
3.  **Service (`hubspot_api.py`):** The `get_contact` method sends a GET request to the HubSpot API for the specific contact ID.
4.  **UI (`volunteer_detail.html`):** The view passes the single `contact` object to the `volunteer_detail.html` template, which displays all of that volunteer's properties.

---

### 3. Update (Editing a Volunteer)

This is the flow for modifying an existing volunteer's information. It's a two-part process: displaying the form, and then processing the changes.

#### a. Displaying the Edit Form (GET Request)

1.  **URL (`urls.py`):** `path('contact/<int:contact_id>/update/', views.volunteer_update, name='volunteer_update')`
2.  **View (`views.py`):** The `volunteer_update` function is called. For a GET request, it first fetches the existing contact's data from HubSpot using `hubspot_api.get_contact()`. It then creates a `VolunteerForm` instance and pre-fills it with this data (`form = VolunteerForm(initial=initial_data)`).
3.  **UI (`volunteer_update.html`):** The view renders the `volunteer_update.html` template with the pre-filled form.

#### b. Submitting the Changes (POST Request)

1.  **View (`views.py`):** When the user submits the form, the `volunteer_update` function is called again, this time with the `POST` method. It validates the form, and if it's valid, it calls `hubspot_api.update_contact(contact_id, properties)`.
2.  **Service (`hubspot_api.py`):** The `update_contact` method sends a PATCH request to the HubSpot API with the new data for the specified contact.
3.  **Redirect:** After the update is successful, the view redirects the user to the `volunteer_detail` page to show the updated information.

---

### 4. Delete (Removing a Volunteer)

This is also a two-part process: confirming the deletion, and then performing it.

#### a. Displaying the Confirmation Page (GET Request)

1.  **URL (`urls.py`):** `path('contact/<int:contact_id>/delete/', views.volunteer_delete, name='volunteer_delete')`
2.  **View (`views.py`):** For a GET request, the `volunteer_delete` view fetches the contact from HubSpot so it can display their name on the confirmation page.
3.  **UI (`volunteer_delete_confirm.html`):** The view renders the `volunteer_delete_confirm.html` template.

#### b. Confirming the Deletion (POST Request)

1.  **View (`views.py`):** When the user confirms the deletion, a POST request is sent. The `volunteer_delete` view calls `hubspot_api.delete_contact(contact_id)`. It also finds the corresponding volunteer in the local database (by email) and deletes them.
2.  **Service (`hubspot_api.py`):** The `delete_contact` method sends a DELETE request to the HubSpot API.
3.  **Redirect:** The user is then redirected to the main `volunteer_list` page.

By following this URL-to-UI path, you can trace the execution flow of any feature in the application and understand how the different files work together.
