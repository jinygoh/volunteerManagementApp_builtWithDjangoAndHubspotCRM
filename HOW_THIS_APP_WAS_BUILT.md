# How This App Was Built: A Step-by-Step Journey

This document explains the process of building the HopeHands Volunteer Management application. Think of it like a recipe, where each step adds a new layer to the final dish.

## Phase 1: Building the Foundation (The Backend)

The "backend" is the engine of our application. You don't see it, but it does all the heavy lifting, like storing data and running the business logic. We used a framework called **Django** to build it, which is like using a pre-made toolkit for building web applications.

**Step 1: Setting up the Project**
First, we created a new Django project. This is like laying the foundation for a house. It creates the basic file structure and configuration we need.

**Step 2: Designing the Data Model**
We asked ourselves: "What information do we need to store?" The answer was information about volunteers. We created a "model" (a blueprint for our database) called `Volunteer`. This model defines all the fields we need to store for each volunteer, such as `first_name`, `email`, `status`, etc. This was done in the `hopehands/volunteer/models.py` file.

**Step 3: Creating the Database**
Once we had the blueprint (the model), we told Django to create the actual database based on it. This is a command called "making migrations" and "migrating." It's like giving the blueprint to a construction crew and telling them to build the frame of the house.

**Step 4: Building the API Endpoints**
An "API" (Application Programming Interface) is like a restaurant menu. It's a list of operations that the frontend (the part you see) can request from the backend. We used something called **Django REST Framework** to build our API.

We created several "endpoints" (like items on the menu):
*   A way to get a list of all volunteers.
*   A way to create a new volunteer (for the signup form).
*   Ways to `approve`, `reject`, `update`, and `delete` a volunteer.
*   A way to handle a bulk upload from a CSV file.

This logic was written in the `hopehands/volunteer/api_views.py` file.

**Step 5: Adding Security**
We didn't want just anyone to be able to see and manage the volunteer list. So, we added an authentication system. Only users with a valid username and password (i.e., the HopeHands administrators) can access the main dashboard and manage volunteers. The public signup form, however, was left open for anyone to use.

**Step 6: Connecting to HubSpot**
A key requirement was to connect to an external service called HubSpot. We wrote a special module (`hopehands/volunteer/hubspot_api.py`) that knows how to talk to HubSpot's API. We then integrated this module into our main API views. Now, when an admin approves a volunteer, the backend automatically sends that volunteer's information to HubSpot.

## Phase 2: Building the User Interface (The Frontend)

The "frontend" is the part of the application that users see and interact with in their web browser. We used a popular library called **React** to build it. React is great for building modern, interactive user interfaces.

**Step 1: Setting up the Project**
Just like with the backend, the first step was to create a new React project. This gives us the initial file structure for our frontend code.

**Step 2: Creating Reusable Components**
In React, you build interfaces by creating small, reusable pieces called "components." We created components for things like buttons, forms, and navigation bars.

**Step 3: Building the Pages**
Once we had our basic components, we assembled them into full pages. We created several pages:
*   `LoginPage.jsx`: For admins to log in.
*   `SignupPage.jsx`: The public form for new volunteers.
*   `DashboardPage.jsx`: The main page where admins see and manage the list of volunteers.
*   `EditVolunteerPage.jsx`: A form to update a volunteer's information.
*   `UploadCsvPage.jsx`: A page for uploading a CSV file.

**Step 4: Connecting the Frontend to the Backend**
The frontend needs to talk to the backend's API to get data and perform actions. We created a special file, `frontend/src/services/api.js`, to handle all this communication.

For example, when an admin clicks the "Approve" button on the `DashboardPage`, the page calls a function from `api.js`. That function then sends the `approve` request to our Django backend's API.

**Step 5: Managing Application State**
"State" is the data that the application needs to keep track of at any given moment. For example, the list of volunteers displayed on the dashboard is part of the state. We used React's "Context" feature (`AuthContext.jsx`) to manage important global state, like whether a user is currently logged in.

## Phase 3: Bringing It All Together

The final step was to make sure the frontend and backend could work together seamlessly. We configured the development server so that when the React frontend makes an API call to a path like `/api/volunteers/`, it gets automatically forwarded to the Django backend server.

And that's how the application was built! It's a combination of a powerful backend engine and a user-friendly frontend interface, working together to solve a real-world problem for HopeHands.
