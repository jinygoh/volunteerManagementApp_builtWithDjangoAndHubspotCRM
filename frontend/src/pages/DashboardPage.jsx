import React, { useState, useEffect } from 'react';
import { getVolunteers, approveVolunteer, rejectVolunteer } from '../services/api';

/**
 * The main dashboard page for administrators.
 * This component fetches and displays the list of all volunteer applications.
 * It allows admins to approve or reject pending applications.
 */
const DashboardPage = () => {
  // State to hold the list of volunteers fetched from the API
  const [volunteers, setVolunteers] = useState([]);
  // State to hold any error messages during API calls
  const [error, setError] = useState('');

  /**
   * Fetches the list of volunteers from the backend API and updates the state.
   */
  const fetchVolunteers = async () => {
    try {
      const response = await getVolunteers();
      setVolunteers(response.data);
    } catch (err) {
      setError('Failed to fetch volunteers. You may need to log in.');
      console.error(err);
    }
  };

  // The useEffect hook runs once when the component mounts.
  // It calls fetchVolunteers to populate the initial list.
  useEffect(() => {
    fetchVolunteers();
  }, []); // The empty dependency array ensures this runs only once on mount.

  /**
   * Handles the click of the "Approve" button for a volunteer.
   * @param {number} id - The ID of the volunteer to approve.
   */
  const handleApprove = async (id) => {
    try {
      await approveVolunteer(id);
      fetchVolunteers(); // Refresh the list to show the updated status
    } catch (err) {
      console.error('Failed to approve volunteer', err);
    }
  };

  /**
   * Handles the click of the "Reject" button for a volunteer.
   * @param {number} id - The ID of the volunteer to reject.
   */
  const handleReject = async (id) => {
    try {
      await rejectVolunteer(id);
      fetchVolunteers(); // Refresh the list to show the updated status
    } catch (err) {
      console.error('Failed to reject volunteer', err);
    }
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {volunteers.map((volunteer) => (
            <tr key={volunteer.id}>
              <td>{volunteer.name}</td>
              <td>{volunteer.email}</td>
              <td>{volunteer.status}</td>
              <td>
                {/* Only show actions for volunteers with a 'pending' status */}
                {volunteer.status === 'pending' && (
                  <>
                    <button onClick={() => handleApprove(volunteer.id)}>Approve</button>
                    <button onClick={() => handleReject(volunteer.id)}>Reject</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DashboardPage;
