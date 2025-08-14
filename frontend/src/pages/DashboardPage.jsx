import React, { useState, useEffect } from 'react';
import { getVolunteers, approveVolunteer, rejectVolunteer } from '../services/api';

const DashboardPage = () => {
  const [volunteers, setVolunteers] = useState([]);
  const [error, setError] = useState('');

  const fetchVolunteers = async () => {
    try {
      const response = await getVolunteers();
      setVolunteers(response.data);
    } catch (err) {
      setError('Failed to fetch volunteers. You may need to log in.');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchVolunteers();
  }, []);

  const handleApprove = async (id) => {
    try {
      await approveVolunteer(id);
      fetchVolunteers(); // Refresh the list
    } catch (err) {
      console.error('Failed to approve volunteer', err);
    }
  };

  const handleReject = async (id) => {
    try {
      await rejectVolunteer(id);
      fetchVolunteers(); // Refresh the list
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
