/**
 * @file UploadCsvPage.jsx
 * @description This component provides a page for administrators to upload a CSV file of volunteers for batch creation.
 *
 * It features a file input and an upload button. On submission, it sends the
 * selected CSV file to the backend API. It displays success and error messages
 * returned from the server.
 */
import React, { useState } from 'react';
import { uploadCsv } from '../services/api';

/**
 * The main component for the CSV upload page.
 * @returns {JSX.Element} The rendered CSV upload page.
 */
const UploadCsvPage = () => {
  // State for the selected file, and for success/error messages.
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  /**
   * Handles changes to the file input element.
   * @param {React.ChangeEvent<HTMLInputElement>} e - The file input change event.
   */
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  /**
   * Handles the form submission for uploading the CSV file.
   * @param {React.FormEvent} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    setMessage('');
    setError('');
    try {
      // Call the upload API function.
      const response = await uploadCsv(file);
      setMessage(response.data.status || 'CSV uploaded successfully!');
      // Display any errors that occurred on specific rows.
      if (response.data.errors && response.data.errors.length > 0) {
        setError(`Some rows could not be imported: ${response.data.errors.join(', ')}`);
      }
    } catch (err) {
      setError('An error occurred during the file upload.');
      console.error(err);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-8 col-lg-6">
        <div className="form-container">
          <h1 className="text-center mb-4">Upload Volunteers CSV</h1>
          {message && <div className="alert alert-success">{message}</div>}
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="csv-file" className="form-label">CSV File</label>
              <input type="file" id="csv-file" className="form-control" accept=".csv" onChange={handleFileChange} required />
            </div>
            <div className="d-grid">
              <button type="submit" className="btn btn-primary">Upload CSV</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UploadCsvPage;
