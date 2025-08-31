/**
 * @file VisualizationPage.jsx
 * @description This page displays volunteer data visualizations.
 *
 * This component fetches aggregated volunteer data from the API and uses
 * Chart.js to render a bar chart illustrating the distribution of volunteers
 * across different preferred roles. It handles loading and error states
 * during the data fetching process.
 */
import React, { useState, useEffect } from 'react';
import api from '../services/api'; // Corrected import
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register the necessary components for a bar chart
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const VisualizationPage = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch data from the visualization endpoint
                const response = await api.get('/visualizations/volunteer-roles/');
                const data = response.data;

                // Transform the API data into the format required by Chart.js
                const transformedData = {
                    labels: data.map(item => item.preferred_volunteer_role),
                    datasets: [
                        {
                            label: 'Number of Volunteers',
                            data: data.map(item => item.count),
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                        },
                    ],
                };

                setChartData(transformedData);
            } catch (err) {
                setError('Failed to fetch visualization data. Please try again later.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Chart.js options for styling and configuration
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Volunteers by Preferred Role',
                font: {
                    size: 20
                }
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Volunteers'
                }
            },
            x: {
               title: {
                    display: true,
                    text: 'Preferred Role'
                }
            }
        }
    };

    if (loading) {
        return <div className="text-center"><p>Loading visualizations...</p></div>;
    }

    if (error) {
        return <div className="alert alert-danger" role="alert">{error}</div>;
    }

    return (
        <div className="container mt-5">
            <h1 className="mb-4 text-center">Volunteer Data Visualization</h1>
            {chartData ? (
                <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                    <Bar data={chartData} options={options} />
                </div>
            ) : (
                <p className="text-center">No data available to display.</p>
            )}
        </div>
    );
};

export default VisualizationPage;
