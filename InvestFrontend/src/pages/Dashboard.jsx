import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapComponent from '../component/mapComponent';
import Navbar from '../component/Navbar';
import Sidebar from '../component/Sidebar';
import Loader from '../component/Loader';
import '../style/layout.css';
import Toast from '../component/Toast';

const Dashboard = () => {
  const [polygonData, setPolygonData] = useState(null);
  const [buffersData, setBufferData] = useState({
    bufferClinics: null,
    bufferRestaut: null,
    bufferBanks: null,
    bufferClubs: null,
    bufferParkdata: null,
    bufferHotels: null,
    hotelType: null,
    stars: null,
  });
  const [geoJsonData, setGeoJsonData] = useState();
  const [showLegend, setShowLegend] = useState(false);
  const [loadingButton, setLoadingButton] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '', type: '' });
  const [isLoading, setIsLoading] = useState(true); // New state for loader
  const [showButtonReport, setshowButtonReport]=useState(false)
  useEffect(() => {
    // Show the loader for 3 seconds
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 4000); // 3 seconds

    return () => clearTimeout(timer); // Cleanup the timer on unmount
  }, []);

  const handlePolygonCreate = (geoJsonData) => {
    setPolygonData(geoJsonData);
  };

  const findsuitableArea = async () => {
    setLoadingButton(true);
    if (polygonData && buffersData) {
      buffersData['region'] = polygonData.geometry;
      const apiUrl = 'http://127.0.0.1:8000/api/suitable_area/';
      try {
        const response = await axios.post(apiUrl, buffersData);
        console.log(response.data);
        setGeoJsonData(response.data);
        setShowLegend(true);
        setToast({ show: true, message: 'Suitable area found!', type: 'success' });
        setshowButtonReport(true)
      } catch (error) {
        console.error('Error:', error);
        setToast({ show: true, message: 'Error fetching suitable area', type: 'error' });
      }
    } else {
      setToast({ show: true, message: 'No data provided', type: 'warning' });
    }
    setLoadingButton(false);
  };

  // Render the loader if isLoading is true, otherwise render the dashboard content
  if (isLoading) {
    return <Loader />;
  }

  return (
    <>
      <Navbar />
      <div className="container">
        <Sidebar
          findsuitableArea={findsuitableArea}
          setBufferData={setBufferData}
          buffersData={buffersData}
          data={geoJsonData}
          polygonData={polygonData?.geometry}
          loadingButton={loadingButton}
          showButtonReport={showButtonReport}
        />
        <div className="main-content">
          <MapComponent
            onPolygonCreate={handlePolygonCreate}
            geoJsonData={geoJsonData}
            showLegend={showLegend}
          />
        </div>
      </div>
      <Toast
        type={toast.type}
        message={toast.message}
        show={toast.show}
        onClose={() => setToast({ show: false, message: '', type: '' })}
      />
    </>
  );
};

export default Dashboard;
