/**
 * @file DashboardPage.jsx
 * @description File Purpose: This component serves as the main administrative
 * interface for managing volunteer applications.
 *
 * This is a "Page" component, meaning it represents a full page view in the
 * application. Its primary responsibilities are:
 * 1.  Fetching and displaying the list of all volunteers from the backend API.
 * 2.  Providing administrators with actions to `approve`, `reject`, `edit`,
 *     and `delete` volunteers.
 * 3.  Displaying feedback messages (e.g., an error if fetching fails).
 *
 * @relationship
 * - It imports and uses several functions from `../services/api.js` to communicate
 *   with the backend.
 * - It uses the `Link` component from `react-router-dom` to navigate to the
 *   `EditVolunteerPage` (or a similar admin edit page).
 * - This component is rendered by the main `App.jsx` when an admin-only route
 *   is accessed.
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getVolunteers, approveVolunteer, rejectVolunteer, deleteVolunteer } from '../services/api';

/**
 * Function: getStatusBadge
 * @description A helper function that returns a Bootstrap CSS class string to
 * color-code the status badge. This keeps the rendering logic in the main
 * component cleaner.
 * @param {string} status - The status of the volunteer ('pending', 'approved', 'rejected').
 * @returns {string} The corresponding Bootstrap background color class.
 */
const getStatusBadge = (status) => {
    // Line: Use a switch statement to check the status value.
    switch (status) {
        case 'pending':
            return 'bg-warning text-dark'; // Yellow badge for pending
        case 'approved':
            return 'bg-success'; // Green badge for approved
        case 'rejected':
            return 'bg-danger'; // Red badge for rejected
        default:
            return 'bg-secondary'; // Grey badge for any other status
    }
}

/**
 * Component: DashboardPage
 * @description The main component for the admin dashboard page.
 * @returns {JSX.Element} The rendered dashboard page.
 */
const DashboardPage = () => {
  // --- Component State ---
  // `useState` is a React Hook that lets you add a "state variable" to a component.

  // Line: `volunteers` state: an array to hold the list of volunteers fetched from the API.
  const [volunteers, setVolunteers] = useState([]);
  // Line: `error` state: a string to display an error message if something goes wrong.
  const [error, setError] = useState('');

  /**
   * Function: fetchVolunteers
   * @description An asynchronous function to fetch volunteer data from the API
   * and update the component's state.
   */
  const fetchVolunteers = async () => {
    try {
      // Line: Call the `getVolunteers` function from our api service.
      const response = await getVolunteers();
      // Line: The API response from Django REST Framework might be paginated, meaning the
      // list of items is inside a `results` key. We check for this structure first.
      if (response.data && Array.isArray(response.data.results)) {
        // Line: If paginated, update state with the `results` array.
        setVolunteers(response.data.results);
      } else if (Array.isArray(response.data)) {
        // Line: If the response is just a simple array, use it directly.
        setVolunteers(response.data);
      } else {
        // Line: If the format is unexpected, log an error and clear the list.
        console.error("Unexpected API response format:", response.data);
        setVolunteers([]);
      }
    } catch (err) {
      // Line: If the API call fails, set an error message to be displayed to the user.
      setError('Failed to fetch volunteers. You may need to log in again.');
      // Line: Log the detailed error to the browser's console for debugging.
      console.error(err);
    }
  };

  // --- Side Effects ---
  // `useEffect` is a React Hook for handling actions that interact with the outside world.
  // This `useEffect` runs once when the component is first added to the screen.
  useEffect(() => {
    // Line: Call our function to fetch the initial list of volunteers.
    fetchVolunteers();
  }, []); // The empty array `[]` means this effect runs only once on mount.

  /**
   * Function: handleApprove
   * @description Event handler for the "Approve" button click.
   * @param {number} id - The ID of the volunteer to approve.
   */
  const handleApprove = async (id) => {
    try {
      // Line: Call the `approveVolunteer` API function with the volunteer's ID.
      await approveVolunteer(id);
      // Line: After a successful action, re-fetch the volunteer list to show the updated status.
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to approve volunteer', err);
    }
  };

  /**
   * Function: handleReject
   * @description Event handler for the "Reject" button click.
   * @param {number} id - The ID of the volunteer to reject.
   */
  const handleReject = async (id) => {
    try {
      // Line: Call the `rejectVolunteer` API function.
      await rejectVolunteer(id);
      // Line: Refresh the list to show the updated status.
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to reject volunteer', err);
    }
  };

  /**
   * Function: handleDelete
   * @description Event handler for the "Delete" button click.
   * This action also triggers a sync to HubSpot to archive the contact.
   * It prompts the admin for confirmation before proceeding.
   * @param {number} id - The ID of the volunteer to delete.
   */
  const handleDelete = async (id) => {
    // Line: Show a confirmation dialog to prevent accidental deletion.
    if (window.confirm('Are you sure you want to permanently delete this volunteer?')) {
      try {
        // Line: If confirmed, call the `deleteVolunteer` API function.
        await deleteVolunteer(id);
        // Line: Refresh the list to remove the deleted volunteer from the UI.
        fetchVolunteers();
      } catch (err) {
        console.error('Failed to delete volunteer', err);
        setError('Failed to delete volunteer. Please try again.');
      }
    }
  };

  // Line: The `return` statement contains the JSX that defines the component's UI.
  return (
    <div>
      <h1 className="text-center my-4">Volunteer Dashboard</h1>
      {/* Line: Conditionally render the error message div only if `error` is not empty. */}
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="card shadow-sm">
        <div className="card-body">
            <div className="table-responsive">
                <table className="table table-striped table-hover">
                    <thead className="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Role</th>
                        <th>Availability</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {/* Line: Check if there are any volunteers to display. */}
                    {volunteers.length > 0 ? volunteers.map((volunteer) => (
                        // `key` is a special prop that helps React identify which items have changed.
                        <tr key={volunteer.id}>
                          <td>{volunteer.id}</td>
                          <td>{volunteer.first_name}</td>
                          <td>{volunteer.last_name}</td>
                          <td>{volunteer.email}</td>
                          <td>{volunteer.phone_number}</td>
                          <td>{volunteer.preferred_volunteer_role}</td>
                          <td>{volunteer.availability}</td>
                          <td>
                              {/* Line: Display a colored badge based on the volunteer's status. */}
                              <span className={`badge ${getStatusBadge(volunteer.status)}`}>
                                  {volunteer.status}
                              </span>
                          </td>
                          <td>
                              {/* Line: Conditionally render the Approve/Reject buttons only if the status is 'pending'. */}
                              {volunteer.status === 'pending' && (
                                  <>
                                      <button className="btn btn-success btn-sm me-2" onClick={() => handleApprove(volunteer.id)}>Approve</button>
                                      <button className="btn btn-danger btn-sm me-2" onClick={() => handleReject(volunteer.id)}>Reject</button>
                                  </>
                              )}
                              {/* Line: The Edit and Delete buttons are always available for all statuses. */}
                              {/* The Link component will navigate the user to the edit page for this volunteer. */}
                              <Link to={`/admin/volunteer/${volunteer.id}/edit`} className="btn btn-primary btn-sm me-2">Edit</Link>
                              <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(volunteer.id)}>Delete</button>
                          </td>
                        </tr>
                    )) : (
                        // Line: If the volunteers array is empty, display a message in a single table row.
                        <tr>
                            <td colSpan="9" className="text-center">No volunteers found.</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
