# Project Overview for Non-Programmers

Welcome! This document explains the HopeHands Volunteer Management application in a simple, non-technical way.

## 1. What is this Project's Goal?

The main goal of this project is to make it easier for the HopeHands organization to manage new volunteer applications.

Before this application, managing signups might have been done manually (e.g., through emails or spreadsheets). This application automates the process and keeps the data organized in one central place.

Think of it as a digital inbox and filing system specifically for volunteer applications.

## 2. What are the Main Parts of the Application?

The application is split into two main parts that work together:

*   **The Frontend (What you see)**: This is the website that users interact with. It includes the signup form for new volunteers and the dashboard that the HopeHands administrators use to manage applications.
*   **The Backend (The engine room)**: This is the part of the application that you don't see. It works behind the scenes to store the data and handle the logic (like approving or rejecting an application).

## 3. How Does it Work? (The Volunteer's Journey)

The process for handling a new volunteer application is simple and can be broken down into a few key steps:

**Step 1: A New Volunteer Signs Up**
A person who wants to volunteer goes to the HopeHands public website and fills out a signup form with their name, email, and other details. When they click "submit," their application is sent to our system.

**Step 2: The Application is Stored**
The application is saved in the application's private database with a "Pending" status, waiting for a review from a HopeHands administrator.

**Step 3: An Admin Reviews the Application**
A HopeHands administrator logs into a private, password-protected dashboard. On this dashboard, they can see a list of all the pending applications. They can review the details of each applicant to decide if they are a good fit.

**Step 4: The Admin Makes a Decision**
The administrator has two choices for each application:
*   **Approve**: If the administrator approves the application, its status is simply changed to "Approved" in the system.
*   **Reject**: If the application is not a good fit, the administrator can reject it. The status is changed to "Rejected."

This workflow ensures that administrators have a clear view of which applications are pending, which have been approved, and which have been rejected.

**Step 5: Managing Approved Volunteers**

Once a volunteer is approved, their journey with HopeHands is just beginning! The administrators can continue to manage their information:

*   **Updating Information**: If a volunteer's details change (e.g., they have a new phone number or change their availability), an administrator can update their profile in the dashboard.
*   **Removing a Volunteer**: If a volunteer leaves the organization, an administrator can delete their record from the dashboard.

## 4. Other Key Features

Besides the main workflow, the application has a couple of other important features for administrators:

*   **CSV Bulk Import**: If an administrator has a list of pre-approved volunteers in a spreadsheet (a CSV file), they can upload it directly into the system. The application will automatically add all of them to the database with an "Approved" status in one go. This is a huge time-saver.
*   **Data Visualization**: The application includes a "Visualizations" page where administrators can see a simple chart showing which volunteer roles are the most popular among applicants. This helps the organization understand what kind of work people are most interested in.
