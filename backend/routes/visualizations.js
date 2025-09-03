const express = require('express');
const router = express.Router();
const Volunteer = require('../models/Volunteer');
const authMiddleware = require('../middleware/authMiddleware');

// All routes in this file are protected
router.use(authMiddleware);

// @route   GET api/visualizations/volunteer-roles
// @desc    Get count of volunteers per role for charts
// @access  Private
router.get('/volunteer-roles', async (req, res) => {
  try {
    const roleData = await Volunteer.aggregate([
      {
        $group: {
          _id: '$preferred_volunteer_role',
          count: { $sum: 1 },
        },
      },
      {
        $project: {
          preferred_volunteer_role: '$_id',
          count: 1,
          _id: 0,
        }
      },
      {
        $sort: { count: -1 },
      },
    ]);
    res.json(roleData);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
