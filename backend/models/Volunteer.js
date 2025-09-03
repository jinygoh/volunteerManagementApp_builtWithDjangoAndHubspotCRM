const mongoose = require('mongoose');

const volunteerSchema = new mongoose.Schema({
  first_name: {
    type: String,
    required: true,
    trim: true,
  },
  last_name: {
    type: String,
    required: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
  },
  phone_number: {
    type: String,
    required: true,
  },
  preferred_volunteer_role: {
    type: String,
    required: true,
  },
  availability: {
    type: String,
    required: true,
  },
  how_did_you_hear_about_us: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    enum: ['pending', 'approved', 'rejected'],
    default: 'pending',
  },
}, {
  timestamps: true, // Adds createdAt and updatedAt timestamps
});

const Volunteer = mongoose.model('Volunteer', volunteerSchema);

module.exports = Volunteer;
