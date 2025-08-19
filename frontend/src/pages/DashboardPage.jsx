/**
 * @file DashboardPage.jsx
 * @description This page displays a list of all volunteer applications for administrators.
 *
 * It fetches the list of volunteers from the API and displays them in a table.
 * Admins can view the status of each application and have options to "Approve" or
 * "Reject" pending applications. The component handles the API calls for these
 * actions and updates the list upon completion.
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getVolunteers, approveVolunteer, rejectVolunteer, deleteVolunteer } from '../services/api';

/**
 * A helper function to determine the Bootstrap badge class based on volunteer status.
 * @param {string} status - The status of the volunteer ('pending', 'approved', 'rejected').
 * @returns {string} The corresponding Bootstrap background color class.
 */
const getStatusBadge = (status) => {
    switch (status) {
        case 'pending':
            return 'bg-warning text-dark';
        case 'approved':
            return 'bg-success';
        case 'rejected':
            return 'bg-danger';
        default:
            return 'bg-secondary';
    }
}

/**
 * The main component for the admin dashboard page.
 * @returns {JSX.Element} The rendered dashboard page.
 */
const DashboardPage = () => {
  const [volunteers, setVolunteers] = useState([]);
  const [error, setError] = useState('');

  /**
   * Fetches the list of volunteers from the server and updates the state.
   */
  const fetchVolunteers = async () => {
    try {
      const response = await getVolunteers();
      // The API response might be paginated by DRF, so check for a 'results' key.
      if (response.data && Array.isArray(response.data.results)) {
        setVolunteers(response.data.results);
      } else if (Array.isArray(response.data)) {
        // Handle non-paginated response
        setVolunteers(response.data);
      } else {
        console.error("Unexpected API response format:", response.data);
        setVolunteers([]);
      }
    } catch (err) {
      setError('Failed to fetch volunteers. You may need to log in again.');
      console.error(err);
    }
  };

  // The useEffect hook runs once when the component mounts to fetch initial data.
  useEffect(() => {
    fetchVolunteers();
  }, []);

  /**
   * Handles the approval of a volunteer.
   * @param {number} id - The ID of the volunteer to approve.
   */
  const handleApprove = async (id) => {
    try {
      await approveVolunteer(id);
      // Refresh the list to show the updated status.
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to approve volunteer', err);
    }
  };

  /**
   * Handles the rejection of a volunteer.
   * @param {number} id - The ID of the volunteer to reject.
   */
  const handleReject = async (id) => {
    try {
      await rejectVolunteer(id);
      // Refresh the list to show the updated status.
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to reject volunteer', err);
    }
  };

  /**
   * Handles the deletion of a volunteer.
   * Prompts the admin for confirmation before proceeding.
   * @param {number} id - The ID of the volunteer to delete.
   */
  const handleDelete = async (id) => {
    // Confirm with the user before deleting
    if (window.confirm('Are you sure you want to permanently delete this volunteer?')) {
      try {
        await deleteVolunteer(id);
        // Refresh the list to remove the deleted volunteer.
        fetchVolunteers();
      } catch (err) {
        console.error('Failed to delete volunteer', err);
        setError('Failed to delete volunteer. Please try again.');
      }
    }
  };

  return (
    <div>
      <h1 className="text-center my-4">Volunteer Dashboard</h1>
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
                    {volunteers.length > 0 ? volunteers.map((volunteer) => (
                        <tr key={volunteer.id}>
                        <td>{volunteer.id}</td>
                        <td>{volunteer.first_name}</td>
                        <td>{volunteer.last_name}</td>
                        <td>{volunteer.email}</td>
                        <td>{volunteer.phone_number}</td>
                        <td>{volunteer.preferred_volunteer_role}</td>
                        <td>{volunteer.availability}</td>
                        <td>
                            <span className={`badge ${getStatusBadge(volunteer.status)}`}>
                                {volunteer.status}
                            </span>
                        </td>
                        <td>
                            {/* Conditional actions for pending volunteers */}
                            {volunteer.status === 'pending' && (
                                <>
                                    <button className="btn btn-success btn-sm me-2" onClick={() => handleApprove(volunteer.id)}>Approve</button>
                                    <button className="btn btn-danger btn-sm" onClick={() => handleReject(volunteer.id)}>Reject</button>
                                </>
                            )}
                            {/* Edit and Delete buttons are always available */}
                            <Link to={`/admin/volunteer/${volunteer.id}/edit`} className="btn btn-primary btn-sm me-2">Edit</Link>
                            <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(volunteer.id)}>Delete</button>
                        </td>
                        </tr>
                    )) : (
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
