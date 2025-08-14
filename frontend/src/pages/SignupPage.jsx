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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(formData);
      setMessage('Thank you for signing up! Your application will be reviewed.');
      setFormData({ name: '', email: '', phone_number: '', preferred_volunteer_role: '', availability: '', how_did_you_hear_about_us: '' });
    } catch (error) {
      setMessage('There was an error submitting your application. Please try again.');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Volunteer Signup</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Phone Number:</label>
          <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
        </div>
        <div>
          <label>Preferred Role:</label>
          <input type="text" name="preferred_volunteer_role" value={formData.preferred_volunteer_role} onChange={handleChange} required />
        </div>
        <div>
          <label>Availability:</label>
          <input type="text" name="availability" value={formData.availability} onChange={handleChange} required />
        </div>
        <div>
            <label>How did you hear about us?:</label>
            <input type="text" name="how_did_you_hear_about_us" value={formData.how_did_you_hear_about_us} onChange={handleChange} />
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
};

export default SignupPage;
