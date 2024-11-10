import React, { useRef } from 'react';
import '../style/AnalysisModal.css';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import GeoDataDisplay from './GeoDataDisplay';
import HotelCharts from './HotelCharts';

const AnalysisModal = ({ show, onClose, title, subtitles, data, polygonData }) => {

    if (!show) {
        return null;
    }

    const handleDownloadPDF = () => {
        const input = document.getElementById('modal-content');
        html2canvas(input)
            .then((canvas) => {
                const imgData = canvas.toDataURL('image/png');
                const pdf = new jsPDF('p', 'mm', 'a4');
                const imgWidth = 210;
                const pageHeight = 295;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                let heightLeft = imgHeight;
                let position = 0;

                pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;

                while (heightLeft >= 0) {
                    position = heightLeft - imgHeight;
                    pdf.addPage();
                    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                    heightLeft -= pageHeight;
                }

                pdf.save(`${title}.pdf`);
            });
    };

    const reportTemplateRef = useRef(null);

    const handleGeneratePdf = () => {
        const doc = new jsPDF({
            format: 'a4',
            unit: 'px',
        });

        doc.setFont('Inter-Regular', 'normal');

        doc.html(reportTemplateRef.current, {
            async callback(doc) {
                await doc.save('document');
            },
        });
    };

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" id="modal-content" onClick={e => e.stopPropagation()}>
                {/* <button className="close-button" onClick={onClose}>
                    &times;
                </button> */}
                <button className="download-button" onClick={handleGeneratePdf}>
                    Download PDF
                </button>
                <div ref={reportTemplateRef}>
                    <h2 className="modal-title">{title}</h2>
                    <div className="modal-body">
                        {data &&
                            <>
                                <HotelCharts region={polygonData} />
                                <GeoDataDisplay
                                    data={data?.hotels}
                                    text={'This section displays the hotels in the selected region, including their locations and buffers.'}
                                    title={'Hotels'}
                                    color={'ForestGreen'}
                                    typeData={'hotels'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.parks}
                                    text={'This section displays the parks in the selected region, including their locations and buffers.'}
                                    title={'Parks'}
                                    color={'Navy'}
                                    typeData={'parks'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.restaurants}
                                    text={'This section displays the restaurants in the selected region, including their locations and buffers.'}
                                    title={'Restaurants'}
                                    color={'LightSkyBlue'}
                                    typeData={'restaurants'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.clubs}
                                    text={'This section displays the clubs in the selected region, including their locations and buffers.'}
                                    title={'Clubs'}
                                    color={'MediumVioletRed'}
                                    typeData={'clubs'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.clinics}
                                    text={'This section displays the clinics in the selected region, including their locations and buffers.'}
                                    title={'Clinics'}
                                    color={'DarkViolet'}
                                    typeData={'clinics'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.banks}
                                    text={'This section displays the banks in the selected region, including their locations and buffers.'}
                                    title={'Banks'}
                                    color={'Purple'}
                                    typeData={'banks'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.suitable_area}
                                    text={'This section shows the suitable areas for development in the selected region, considering the existing structures and buffers.'}
                                    title={'Suitable Areas with Buildings'}
                                    color={'SeaGreen'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.buildings}
                                    text={'This section displays the buildings in the selected region, including their locations and buffers.'}
                                    title={'Buildings in Your Region'}
                                    color={'Brown'}
                                    center={data?.center}
                                />
                                <GeoDataDisplay
                                    data={data?.suitable_area_no_buildings}
                                    text={'This section shows the areas that are suitable for development with no existing buildings, based on the buffers and existing data.'}
                                    title={'Suitable Areas Without Buildings'}
                                    color={'DarkGreen'}
                                    center={data?.center}
                                />
                            </>
                        }
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AnalysisModal;
