# Crash Course: HopeHands Volunteer Signup Application

This document provides a high-level overview of the HopeHands Volunteer Signup application.

## 1. Purpose

The HopeHands application is a web-based platform designed to streamline the volunteer signup process. It allows potential volunteers to register their interest in volunteering with the organization by providing their contact information and preferences. The application also integrates with HubSpot, a popular Customer Relationship Management (CRM) platform, to automatically add new volunteers as contacts in the organization's HubSpot account.

## 2. Features

*   **Volunteer Signup Form:** A user-friendly form for collecting volunteer information, including:
    *   Name
    *   Email
    *   Phone Number
    *   Preferred Volunteer Role
    *   Availability
    *   How they heard about the organization
*   **HubSpot Integration:** Automatically creates a new contact in HubSpot for each new volunteer who signs up. This helps the organization manage its volunteers and track their engagement.
*   **Success Page:** A confirmation page that lets the user know their submission was successful.

## 3. Technology Stack

The application is built using the following technologies:

*   **Backend:**
    *   **Python:** The primary programming language.
    *   **Django:** A high-level Python web framework that provides the application's structure.
    *   **MySQL:** The relational database used to store volunteer data.
    *   **hubspot-api-client:** The official Python client for the HubSpot API.
*   **Frontend:**
    *   **HTML:** The markup language for creating the web pages.
    *   **CSS:** Used for styling the application (though minimal in the current version).
*   **Environment:**
    *   The application's dependencies are managed using `pip` and a `requirements.txt` file.
    *   Environment variables are used to store sensitive information like API keys and database credentials.
