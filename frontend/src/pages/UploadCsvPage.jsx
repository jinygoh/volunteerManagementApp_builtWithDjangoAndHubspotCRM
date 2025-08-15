import React, { useState } from 'react';
import { uploadCsv } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { jwtDecode } from 'jwt-decode';

const UploadCsvPage = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [uploadErrors, setUploadErrors] = useState([]);
    const { authTokens, refreshToken } = useAuth();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }
        setError('');
        setMessage('');
        setUploadErrors([]);

        // Proactive token refresh check
        const user = jwtDecode(authTokens.access);
        const isExpired = Date.now() >= user.exp * 1000;

        if (isExpired) {
            await refreshToken();
        }

        try {
            const response = await uploadCsv(file);
            setMessage(response.data.status || 'File uploaded successfully!');
            setUploadErrors(response.data.errors || []);
            setFile(null);
            e.target.reset();
        } catch (err) {
            setError('An error occurred during the file upload.');
            console.error(err);
        }
    };

    return (
        <div className="row justify-content-center">
            <div className="col-md-8">
                <div className="card shadow-sm mt-5">
                    <div className="card-body form-container">
                        <h2 className="text-center mb-4">Upload Volunteers from CSV</h2>
                        {message && <div className="alert alert-success">{message}</div>}
                        {error && <div className="alert alert-danger">{error}</div>}
                        {uploadErrors.length > 0 && (
                            <div className="alert alert-warning">
                                <h4 className="alert-heading">Upload Issues</h4>
                                <p>The following rows could not be imported:</p>
                                <ul>
                                    {uploadErrors.map((e, index) => (
                                        <li key={index}>{e}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                        <form onSubmit={handleSubmit}>
                            <div className="form-group mb-3">
                                <label htmlFor="csv-file" className="form-label">CSV File</label>
                                <input
                                    type="file"
                                    id="csv-file"
                                    className="form-control"
                                    accept=".csv"
                                    onChange={handleFileChange}
                                />
                            </div>
                            <div className="d-grid">
                                <button type="submit" className="btn btn-primary">Upload File</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadCsvPage;
