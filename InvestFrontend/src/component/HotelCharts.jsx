import React, { useEffect, useState } from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, BarElement, CategoryScale, LinearScale, Legend, Title, Tooltip } from 'chart.js';
import axios from 'axios';
import '../style/HotelCharts.css'; // Import CSS for styling

// Register the necessary components for Chart.js
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Legend, Title, Tooltip);

const HotelCharts = ({ region }) => {
    const [typeData, setTypeData] = useState({});
    const [starData, setStarData] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch data from the API
        const fetchData = async () => {
            await axios.post('http://127.0.0.1:8000/api/hotels_data_chart/', region)
                .then(response => {
                    const { types_count, stars_count } = response.data;
                    console.log(response.data);
                    
                    setTypeData({
                        labels: Object.keys(types_count),
                        datasets: [{
                            label: 'Hotel Types',
                            data: Object.values(types_count),
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                        }]
                    });

                    setStarData({
                        labels: Object.keys(stars_count),
                        datasets: [{
                            label: 'Hotel Stars',
                            data: Object.values(stars_count),
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                        }]
                    });

                    setLoading(false);
                })
                .catch(error => {
                    console.error("Error fetching hotel data:", error);
                });
        };
        fetchData();
    }, [region]);

    const chartOptions = (titleText) => ({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
            },
            title: {
                display: true,
                text: titleText,
                font: {
                    size: 18,
                }
            },
        },
        layout: {
            padding: {
                top: 10,
                bottom: 10,
            },
        },
    });

    return (
        <div className="chart-container">
            {!loading && (
                <>
                    <div className="chart-wrapper">
                        <Bar 
                            data={typeData} 
                            options={chartOptions('Hotel Types Distribution')} 
                        />
                    </div>
                    <div className="chart-wrapper">
                        <Doughnut 
                            data={starData} 
                            options={chartOptions('Hotel Stars Distribution')} 
                        />
                    </div>
                </>
            )}
        </div>
    );
};

export default HotelCharts;
