import React, { useEffect, useState } from 'react';
import '../style/sidebar.css';
import AnalysisModal from '../component/modal';
import EditNoteIcon from '@mui/icons-material/EditNote';
import { Oval } from 'react-loader-spinner'; // Importing a loader


const Sidebar = ({ findsuitableArea, setBufferData, data, polygonData, loadingButton, showButtonReport }) => {
    const [bufferHotel, setBufferHotel] = useState(50);
    const [bufferPark, setBufferPark] = useState(50);
    const [bufferRestaut, setBufferRestaut] = useState(50);
    const [bufferClinics, setBufferClinics] = useState(50);
    const [bufferClubs, setBufferClubs] = useState(50);
    const [bufferBanks, setBufferBanks] = useState(50);
    const [showDetails, setShowDetails] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loadingReport, setLoadingReport] = useState(false); // State for report loader
    const [reportButtonText, setReportButtonText] = useState("Generate Report"); // State for the Report button text

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const title = "Analysis Report";
    const subtitles = ["Subtitle 1", "Subtitle 2", "Subtitle 3"];
    const [hotelTypes, setHotelTypes] = useState({
        hotel: true,
        riad: false,
        hostel: false,
    });
    const [stars, setStars] = useState({
        1: false,
        2: false,
        3: true,
        4: true,
        5: true,
    });

    const toggleDetails = () => setShowDetails(!showDetails);

    useEffect(() => {
        setBufferData((previous) => ({
            ...previous,
            bufferClinics,
            bufferRestaut,
            bufferBanks,
            bufferClubs,
            bufferParkdata: bufferPark,
            bufferHotels: bufferHotel,
            hotelType: Object.keys(hotelTypes).filter((type) => hotelTypes[type]),
            stars: Object.keys(stars).filter((star) => stars[star]).map(Number),
        }));
    }, [bufferClinics, bufferRestaut, bufferBanks, bufferClubs, bufferPark, bufferHotel, stars, hotelTypes]);

    const handleReportClick = () => {
        if (reportButtonText === 'Report') {
            setIsModalOpen(true);
        } else {
            setLoadingReport(true);
            setReportButtonText("Generating...");

            setTimeout(() => {
                setLoadingReport(false);
                setReportButtonText("Report");
            }, 6000); // Simulating a 10-second loading time
        }

    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>Buffer Settings</h2>
                {showButtonReport &&
                    <button onClick={handleReportClick} className="button-main" disabled={loadingReport}>
                        {loadingReport ? (
                            <Oval height={20} width={20} color="white" />
                        ) : (
                            <>
                                <EditNoteIcon style={{ color: 'white' }} />
                                {reportButtonText}
                            </>
                        )}
                    </button>
                }

            </div>
            <hr className="modal-separator" />
            <label>
                Buffer Hotels(meter):
                <input type="number" step="50" value={bufferHotel} onChange={(e) => setBufferHotel(e.target.value)} />
            </label>
            <label>
                Buffer Parks(meter):
                <input type="number" step="50" value={bufferPark} onChange={(e) => setBufferPark(e.target.value)} />
            </label>
            <label>
                Buffer Restaurants(meter):
                <input type="number" step="50" value={bufferRestaut} onChange={(e) => setBufferRestaut(e.target.value)} />
            </label>
            <label>
                Buffer hospitals(meter):
                <input type="number" step="50" value={bufferClinics} onChange={(e) => setBufferClinics(e.target.value)} />
            </label>
            <label>
                Buffer Clubs(meter):
                <input type="number" step="50" value={bufferClubs} onChange={(e) => setBufferClubs(e.target.value)} />
            </label>
            <label>
                Buffer Banks(meter):
                <input type="number" step="50" value={bufferBanks} onChange={(e) => setBufferBanks(e.target.value)} />
            </label>

            <button onClick={toggleDetails} className="accordion-title">
                More Details
                <span className={`arrow ${showDetails ? 'up' : 'down'}`}></span>
            </button>
            {showDetails && (
                <div className="accordion-content">
                    <h3>Hotel Types</h3>
                    {Object.keys(hotelTypes).map((type) => (
                        <label key={type}>
                            <input
                                type="checkbox"
                                checked={hotelTypes[type]}
                                onChange={() => setHotelTypes({ ...hotelTypes, [type]: !hotelTypes[type] })}
                            />
                            {type.charAt(0).toUpperCase() + type.slice(1)}
                        </label>
                    ))}

                    <h3>Stars</h3>
                    {Object.keys(stars).map((star) => (
                        <label key={star}>
                            <input
                                type="checkbox"
                                checked={stars[star]}
                                onChange={() => setStars({ ...stars, [star]: !stars[star] })}
                            />
                            {star} Star
                        </label>
                    ))}
                </div>
            )}

            <button onClick={findsuitableArea} className="generate-button">
                {loadingButton ? (
                    <div className="loader-wrapper">
                        <Oval height={20} width={20} color="white" />
                    </div>
                ) : (
                    "Generate Result"
                )}
            </button>


            <AnalysisModal
                show={isModalOpen}
                onClose={handleCloseModal}
                title={title}
                subtitles={subtitles}
                data={data}
                polygonData={polygonData}
            />
        </div>
    );
};

export default Sidebar;
