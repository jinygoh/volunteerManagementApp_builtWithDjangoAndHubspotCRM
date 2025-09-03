const express = require('express');
const router = express.Router();
const Volunteer = require('../models/Volunteer');

// @route   POST api/signup
// @desc    Create a new volunteer application
// @access  Public
router.post('/', async (req, res) => {
  try {
    const newVolunteer = new Volunteer({
      ...req.body,
      status: 'pending', // Ensure status is pending on new signups
    });

    const volunteer = await newVolunteer.save();
    res.status(201).json(volunteer);
  } catch (err) {
    // Handle potential duplicate email error
    if (err.code === 11000) {
      return res.status(400).json({ msg: 'A volunteer with this email already exists.' });
    }
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
