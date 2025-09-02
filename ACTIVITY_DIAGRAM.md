# Activity Diagrams

This document provides activity diagrams to visualize the main workflows in the HopeHands application. An activity diagram is like a flowchart that shows the steps in a process, including actions taken by different people or systems.

You can copy and paste the code blocks below into a Mermaid-compatible viewer to see the visual diagrams.

---

## 1. New Volunteer Signup and Approval Workflow

This diagram shows the end-to-end process from a new volunteer signing up to an admin approving them.

```mermaid
sequenceDiagram
    participant NewVolunteer as New Volunteer
    participant FrontendApp as Frontend App
    participant BackendAPI as Backend API
    participant AdminUser as Admin User
    participant HubSpot

    NewVolunteer->>+FrontendApp: 1. Fills out and submits signup form
    FrontendApp->>+BackendAPI: 2. Sends new volunteer data
    BackendAPI-->>-FrontendApp: 3. Confirms creation (status: 'pending')
    FrontendApp-->>-NewVolunteer: 4. Shows "Success" message

    Note over AdminUser, HubSpot: Sometime later...

    AdminUser->>+FrontendApp: 5. Logs in and views dashboard
    FrontendApp->>+BackendAPI: 6. Requests list of volunteers
    BackendAPI-->>-FrontendApp: 7. Sends list (including pending volunteer)

    AdminUser->>+FrontendApp: 8. Clicks "Approve" for the new volunteer
    FrontendApp->>+BackendAPI: 9. Sends 'approve' command for volunteer
    BackendAPI->>BackendAPI: 10. Updates volunteer status to 'approved'
    BackendAPI->>+HubSpot: 11. Sends volunteer data to create contact
    HubSpot-->>-BackendAPI: 12. Confirms contact creation with HubSpot ID
    BackendAPI->>BackendAPI: 13. Saves HubSpot ID to volunteer record
    BackendAPI-->>-FrontendApp: 14. Confirms approval was successful

    FrontendApp->>+BackendAPI: 15. Refreshes volunteer list
    BackendAPI-->>-FrontendApp: 16. Sends updated list
    Note over FrontendApp, AdminUser: Dashboard now shows volunteer as 'Approved'
```

### Explanation of the Workflow

1.  **Signup**: A `New Volunteer` submits their information through the `Frontend App`.
2.  **Storage**: The `Backend API` receives this data and stores it in the local database with a status of `pending`.
3.  **Admin Review**: Later, an `Admin User` logs in and sees the list of pending volunteers on their dashboard.
4.  **Approval**: The admin clicks the "Approve" button.
5.  **Backend Action**: The `Backend API` receives the approval command. It performs two key actions:
    *   It updates the volunteer's status to `approved` in its own database.
    *   It sends the volunteer's information to the external `HubSpot` service.
6.  **HubSpot Sync**: HubSpot creates a new contact and returns a unique ID for that contact. The `Backend API` saves this ID so it can link the local record to the HubSpot record.
7.  **UI Update**: The `Frontend App` automatically refreshes its data, and the admin now sees the volunteer's status as "Approved" on the dashboard.

---

## 2. CSV Bulk Upload Workflow

This diagram shows how an admin can upload a list of pre-approved volunteers from a spreadsheet.

```mermaid
sequenceDiagram
    participant AdminUser as Admin User
    participant FrontendApp as Frontend App
    participant BackendAPI as Backend API
    participant HubSpot as HubSpot

    AdminUser->>+FrontendApp: 1. Selects a CSV file and clicks "Upload"
    FrontendApp->>+BackendAPI: 2. Sends the CSV file
    BackendAPI->>BackendAPI: 3. Reads and processes the file row by row
    Note right of BackendAPI: For each row, it prepares a new volunteer record (status: 'approved') and a new HubSpot contact.

    BackendAPI->>BackendAPI: 4. Bulk-creates all new volunteers in local database
    BackendAPI->>+HubSpot: 5. Sends a batch request to create all contacts
    HubSpot-->>-BackendAPI: 6. Returns results of the batch creation
    BackendAPI->>BackendAPI: 7. Updates local volunteer records with their new HubSpot IDs

    BackendAPI-->>-FrontendApp: 8. Sends a summary of the operation (e.g., "50 volunteers created, 50 synced to HubSpot")
    FrontendApp-->>-AdminUser: 9. Displays the success message
```

### Explanation of the Workflow

1.  **Upload**: An `Admin User` uploads a CSV file through the `Frontend App`.
2.  **Processing**: The `Backend API` receives the entire file. It reads the spreadsheet and creates a list of new volunteers to be added. It immediately sets their status to `approved`.
3.  **Bulk Creation**: The backend performs two large operations:
    *   It adds all the new volunteers to its local database in a single, efficient operation.
    *   It sends all the new contacts to `HubSpot` in a single batch request, which is much faster than sending them one by one.
4.  **Sync IDs**: After HubSpot confirms the creation, the `Backend API` updates the newly created local records with their corresponding HubSpot IDs.
5.  **Confirmation**: The `Frontend App` receives a confirmation message from the backend and displays it to the admin.
