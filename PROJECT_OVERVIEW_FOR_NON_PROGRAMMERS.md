# Project Overview for Non-Programmers

Welcome! This document explains the HopeHands Volunteer Management application in a simple, non-technical way.

## 1. What is this Project's Goal?

The main goal of this project is to make it easier for the HopeHands organization to manage new volunteer applications.

Before this application, managing signups might have been done manually (e.g., through emails or spreadsheets). This application automates the process, keeps the data organized, and ensures that only approved volunteers are added to the organization's official contact list in a system called **HubSpot**.

Think of it as a digital inbox and filing system specifically for volunteer applications.

## 2. What are the Main Parts of the Application?

The application is split into two main parts that work together:

*   **The Frontend (What you see)**: This is the website that users interact with. It includes the signup form for new volunteers and the dashboard that the HopeHands administrators use to manage applications.
*   **The Backend (The engine room)**: This is the part of the application that you don't see. It works behind the scenes to store the data, handle the logic (like approving or rejecting an application), and communicate with other systems like HubSpot.

## 3. How Does it Work? (The Volunteer's Journey)

The process for handling a new volunteer application is simple and can be broken down into a few key steps:

**Step 1: A New Volunteer Signs Up**
A person who wants to volunteer goes to the HopeHands public website and fills out a signup form with their name, email, and other details. When they click "submit," their application is sent to our system.

**Step 2: The Application is Stored**
The application is saved in our private database with a "Pending" status. At this point, the information has **not** been sent to the official HubSpot contact list. It's waiting for a review from a HopeHands administrator.

**Step 3: An Admin Reviews the Application**
A HopeHands administrator logs into a private, password-protected dashboard. On this dashboard, they can see a list of all the pending applications. They can review the details of each applicant to decide if they are a good fit.

**Step 4: The Admin Makes a Decision**
The administrator has two choices for each application:
*   **Approve**: If the administrator approves the application, two things happen:
    1. The application's status is changed to "Approved" in our system.
    2. The volunteer's contact information is automatically sent to the official HubSpot system.
*   **Reject**: If the application is not a good fit, the administrator can reject it. The status is simply changed to "Rejected," and the information is **not** sent to HubSpot.

This workflow ensures that the main HubSpot contact list remains clean and only contains information from fully approved volunteers.

## 4. Other Key Features

Besides the main workflow, the application has a couple of other important features for administrators:

*   **CSV Bulk Import**: If an administrator has a list of pre-approved volunteers in a spreadsheet (a CSV file), they can upload it directly into the system. The application will automatically add all of them to the local database and sync them to HubSpot in one go. This is a huge time-saver.
*   **Data Visualization**: The application includes a "Visualizations" page where administrators can see a simple chart showing which volunteer roles are the most popular among applicants. This helps the organization understand what kind of work people are most interested in.
