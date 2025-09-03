const express = require('express');
const router = express.Router();
const multer = require('multer');
const csv = require('csv-parser');
const stream = require('stream');

const Volunteer = require('../models/Volunteer');
const authMiddleware = require('../middleware/authMiddleware');

// All routes in this file are protected
router.use(authMiddleware);

// Configure multer for CSV upload
const upload = multer({ storage: multer.memoryStorage() });

// @route   POST api/volunteers/upload-csv
// @desc    Upload and process a CSV file of volunteers
// @access  Private
router.post('/upload-csv', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ msg: 'No file uploaded' });
  }

  const volunteersToCreate = [];
  const bufferStream = new stream.PassThrough();
  bufferStream.end(req.file.buffer);

  bufferStream
    .pipe(csv({
      mapHeaders: ({ header }) => header.toLowerCase().replace(/ /g, '_').replace('?', '')
    }))
    .on('data', (row) => {
      let { first_name, last_name, email, name } = row;

      if (!email) {
        return; // Skip rows without email
      }

      // Handle cases where name is a single column
      if (name && !first_name && !last_name) {
        const parts = name.split(' ');
        first_name = parts[0];
        last_name = parts.slice(1).join(' ');
      }

      volunteersToCreate.push({
        first_name: first_name || '',
        last_name: last_name || '',
        email: email,
        phone_number: row.phone_number || '',
        preferred_volunteer_role: row.preferred_volunteer_role || '',
        availability: row.availability || '',
        how_did_you_hear_about_us: row.how_did_you_hear_about_us || '',
        status: 'approved', // Volunteers from CSV are auto-approved
      });
    })
    .on('end', async () => {
      try {
        if (volunteersToCreate.length > 0) {
          // Using insertMany for bulk insertion
          await Volunteer.insertMany(volunteersToCreate, { ordered: false });
        }
        res.status(201).json({ msg: `${volunteersToCreate.length} volunteers successfully uploaded and approved.` });
      } catch (err) {
        // We can ignore duplicate key errors if we want to allow re-uploading the same file
        if (err.code === 11000) {
          return res.status(201).json({ msg: 'CSV processed. Some volunteers may already exist.' });
        }
        console.error(err.message);
        res.status(500).send('Server error during database insertion.');
      }
    });
});

// @route   GET api/volunteers
// @desc    Get all volunteers
// @access  Private
router.get('/', async (req, res) => {
  try {
    const volunteers = await Volunteer.find().sort({ createdAt: -1 });
    res.json(volunteers);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// @route   PUT api/volunteers/:id
// @desc    Update a volunteer
// @access  Private
router.put('/:id', async (req, res) => {
  try {
    const volunteer = await Volunteer.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true }
    );
    if (!volunteer) {
      return res.status(404).json({ msg: 'Volunteer not found' });
    }
    res.json(volunteer);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// @route   DELETE api/volunteers/:id
// @desc    Delete a volunteer
// @access  Private
router.delete('/:id', async (req, res) => {
  try {
    const volunteer = await Volunteer.findByIdAndDelete(req.params.id);
    if (!volunteer) {
      return res.status(404).json({ msg: 'Volunteer not found' });
    }
    res.json({ msg: 'Volunteer removed' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// @route   POST api/volunteers/:id/approve
// @desc    Approve a volunteer
// @access  Private
router.post('/:id/approve', async (req, res) => {
  try {
    const volunteer = await Volunteer.findByIdAndUpdate(
      req.params.id,
      { $set: { status: 'approved' } },
      { new: true }
    );
    if (!volunteer) {
      return res.status(404).json({ msg: 'Volunteer not found' });
    }
    res.json(volunteer);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// @route   POST api/volunteers/:id/reject
// @desc    Reject a volunteer
// @access  Private
router.post('/:id/reject', async (req, res) => {
  try {
    const volunteer = await Volunteer.findByIdAndUpdate(
      req.params.id,
      { $set: { status: 'rejected' } },
      { new: true }
    );
    if (!volunteer) {
      return res.status(404).json({ msg: 'Volunteer not found' });
    }
    res.json(volunteer);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
