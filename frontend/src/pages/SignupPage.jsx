import React, { useState } from 'react';
import { signup } from '../services/api';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone_number: '',
    preferred_volunteer_role: '',
    availability: '',
    how_did_you_hear_about_us: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      await signup(formData);
      setMessage('Thank you for signing up! Your application will be reviewed.');
      setFormData({ name: '', email: '', phone_number: '', preferred_volunteer_role: '', availability: '', how_did_you_hear_about_us: '' });
    } catch (err) {
      setError('There was an error submitting your application. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-8 col-lg-6">
        <div className="form-container">
          <h1 className="text-center mb-4">Volunteer Signup</h1>
          {message && <div className="alert alert-success">{message}</div>}
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="name">Name</label>
              <input type="text" id="name" name="name" className="form-control" value={formData.name} onChange={handleChange} required />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="email">Email</label>
              <input type="email" id="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="phone_number">Phone Number</label>
              <input type="text" id="phone_number" name="phone_number" className="form-control" value={formData.phone_number} onChange={handleChange} required />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="preferred_volunteer_role">Preferred Volunteer Role</label>
              <input type="text" id="preferred_volunteer_role" name="preferred_volunteer_role" className="form-control" value={formData.preferred_volunteer_role} onChange={handleChange} required />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="availability">Availability</label>
              <input type="text" id="availability" name="availability" className="form-control" value={formData.availability} onChange={handleChange} required />
            </div>
            <div className="form-group mb-3">
                <label htmlFor="how_did_you_hear_about_us">How did you hear about us?</label>
                <input type="text" id="how_did_you_hear_about_us" name="how_did_you_hear_about_us" className="form-control" value={formData.how_did_you_hear_about_us} onChange={handleChange} />
            </div>
            <div className="d-grid">
                <button type="submit" className="btn btn-primary">Sign Up</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
