import React, { useState, useEffect } from 'react';
import { getVolunteers, approveVolunteer, rejectVolunteer } from '../services/api';

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

const DashboardPage = () => {
  const [volunteers, setVolunteers] = useState([]);
  const [error, setError] = useState('');

  const fetchVolunteers = async () => {
    try {
      const response = await getVolunteers();
      // Ensure response.data is an array before setting state
      if (Array.isArray(response.data)) {
        setVolunteers(response.data);
      } else if (response.data && Array.isArray(response.data.results)) {
        // Handle paginated response from DRF
        setVolunteers(response.data.results);
      } else {
        setVolunteers([]);
      }
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
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to approve volunteer', err);
    }
  };

  const handleReject = async (id) => {
    try {
      await rejectVolunteer(id);
      fetchVolunteers();
    } catch (err) {
      console.error('Failed to reject volunteer', err);
    }
  };

  return (
    <div>
      <h1 className="text-center my-4">Volunteer List</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="card shadow-sm">
        <div className="card-body">
            <table className="table table-striped table-hover">
                <thead className="table-dark">
                <tr>
                    <th>ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email</th>
                    <th>Phone Number</th>
                    <th>Preferred Role</th>
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
                        {volunteer.status === 'pending' && (
                        <>
                            <button className="btn btn-success btn-sm me-2" onClick={() => handleApprove(volunteer.id)}>Approve</button>
                            <button className="btn btn-danger btn-sm" onClick={() => handleReject(volunteer.id)}>Reject</button>
                        </>
                        )}
                    </td>
                    </tr>
                )) : (
                    <tr>
                        <td colSpan="8" className="text-center">No volunteers found.</td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
