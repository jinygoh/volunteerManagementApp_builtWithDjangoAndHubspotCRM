/**
 * @file EditVolunteerPage.jsx
 * @description This page provides a form for administrators to edit the details of a volunteer.
 *
 * It fetches the volunteer's current data based on the ID from the URL, pre-fills the
 * form with this data, and allows the admin to make and submit changes. Upon submission,
 * it calls the API to update the volunteer's record and then redirects the admin
 * back to the main dashboard.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getVolunteers, updateVolunteer } from '../services/api';

/**
 * The main component for the volunteer edit page.
 * @returns {JSX.Element} The rendered edit form.
 */
const EditVolunteerPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [volunteer, setVolunteer] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    preferred_volunteer_role: '',
    availability: '',
    how_did_you_hear_about_us: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  // Fetch the specific volunteer's data when the component mounts.
  useEffect(() => {
    const fetchVolunteer = async () => {
      try {
        // We get the volunteer from the general list and find the one with the matching ID.
        const response = await getVolunteers();
        const allVolunteers = response.data.results || response.data;
        const currentVolunteer = allVolunteers.find(v => v.id.toString() === id);

        if (currentVolunteer) {
          setVolunteer(currentVolunteer);
        } else {
          setError('Volunteer not found.');
        }
      } catch (err) {
        setError('Failed to fetch volunteer data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchVolunteer();
  }, [id]);

  /**
   * Handles changes to the form inputs and updates the component's state.
   * @param {Event} e - The input change event.
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setVolunteer(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  /**
   * Handles the form submission. It calls the API to update the volunteer
   * and then navigates back to the dashboard.
   * @param {Event} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateVolunteer(id, volunteer);
      // After successful update, redirect to the dashboard.
      navigate('/admin/dashboard');
    } catch (err) {
      setError('Failed to update volunteer.');
      console.error(err);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container my-4">
      <div className="card shadow-sm">
        <div className="card-body">
          <h1 className="card-title text-center mb-4">Edit Volunteer</h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="first_name" className="form-label">First Name</label>
              <input type="text" className="form-control" id="first_name" name="first_name" value={volunteer.first_name} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="last_name" className="form-label">Last Name</label>
              <input type="text" className="form-control" id="last_name" name="last_name" value={volunteer.last_name} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">Email</label>
              <input type="email" className="form-control" id="email" name="email" value={volunteer.email} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="phone_number" className="form-label">Phone Number</label>
              <input type="text" className="form-control" id="phone_number" name="phone_number" value={volunteer.phone_number} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="preferred_volunteer_role" className="form-label">Preferred Role</label>
              <input type="text" className="form-control" id="preferred_volunteer_role" name="preferred_volunteer_role" value={volunteer.preferred_volunteer_role} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="availability" className="form-label">Availability</label>
              <input type="text" className="form-control" id="availability" name="availability" value={volunteer.availability} onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label htmlFor="how_did_you_hear_about_us" className="form-label">How did you hear about us?</label>
              <input type="text" className="form-control" id="how_did_you_hear_about_us" name="how_did_you_hear_about_us" value={volunteer.how_did_you_hear_about_us || ''} onChange={handleChange} />
            </div>
            <div className="d-grid gap-2">
                <button type="submit" className="btn btn-primary">Save Changes</button>
                <button type="button" className="btn btn-secondary" onClick={() => navigate('/admin/dashboard')}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditVolunteerPage;
