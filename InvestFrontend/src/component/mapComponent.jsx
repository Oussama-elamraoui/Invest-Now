import React, { useRef, useEffect, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, GeoJSON } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import './mapComponent.css';

const MapComponent = ({ onPolygonCreate, geoJsonData,showLegend }) => {
    const mapRef = useRef();
    const featureGroupRef = useRef();

    const [suitableArea, setSuitableArea] = useState([]);
    const [suitableAreaWithoutbuilding, setSuitableAreaWithoutbuilding] = useState([]);
    const [building, setBuilding] = useState([]);

    // State to track checkbox states
    const [showSuitableArea, setShowSuitableArea] = useState(true);
    const [showSuitableAreaWithoutbuilding, setShowSuitableAreaWithoutbuilding] = useState(true);
    const [showBuilding, setShowBuilding] = useState(true);

    useEffect(() => {
        const map = mapRef.current;
        if (!map) return;

        const drawnItems = new L.FeatureGroup();
        featureGroupRef.current = drawnItems;
        map.addLayer(drawnItems);

        map.on(L.Draw.Event.CREATED, (event) => {
            const layer = event.layer;
            drawnItems.addLayer(layer);
            const geoJsonData = layer.toGeoJSON();
            if (onPolygonCreate) {
                onPolygonCreate(geoJsonData);
            }
        });
    }, [onPolygonCreate]);

    useEffect(() => {
        if (geoJsonData) {
            setSuitableAreaWithoutbuilding((previous) => [...previous, geoJsonData?.suitable_area_no_buildings.geojson]);
            setBuilding((previous) => [...previous, geoJsonData?.buildings?.geojson]);
            setSuitableArea((previous) => [...previous, geoJsonData?.suitable_area?.geojson]);
        }
    }, [geoJsonData]);

    // Legend with checkboxes
    const MapLegend = () => (
        <div className="legend-container">
            <h4>Legend</h4>
            <label className="legend-item">
                <input 
                    type="checkbox" 
                    checked={showSuitableAreaWithoutbuilding} 
                    onChange={() => setShowSuitableAreaWithoutbuilding(!showSuitableAreaWithoutbuilding)} 
                />
                <span className="checkbox-color" style={{ backgroundColor: 'green' }}></span>
                Suitable Areas Without Buildings
            </label>
            <label className="legend-item">
                <input 
                    type="checkbox" 
                    checked={showSuitableArea} 
                    onChange={() => setShowSuitableArea(!showSuitableArea)} 
                />
                <span className="checkbox-color" style={{ backgroundColor: 'blue' }}></span>
                Suitable Areas
            </label>
            <label className="legend-item">
                <input 
                    type="checkbox" 
                    checked={showBuilding} 
                    onChange={() => setShowBuilding(!showBuilding)} 
                />
                <span className="checkbox-color" style={{ backgroundColor: 'red' }}></span>
                Buildings
            </label>
        </div>
    );

    return (
        <div className="map">
            <MapContainer
                center={[37.62856, 4.8144829]}
                zoom={3}
                style={{ height: '850px', width: '100%' }}
                whenCreated={(mapInstance) => { mapRef.current = mapInstance; }}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <FeatureGroup ref={featureGroupRef}>
                    <EditControl
                        position='topright'
                        onCreated={(e) => {
                            const layer = e.layer;
                            featureGroupRef.current.addLayer(layer);
                            const geoJsonData = layer.toGeoJSON();
                            if (onPolygonCreate) {
                                onPolygonCreate(geoJsonData);
                            }
                        }}
                        draw={{
                            rectangle: false,
                            circle: false,
                            polyline: false,
                            marker: false,
                            circlemarker: false,
                        }}
                        edit={{
                            featureGroup: featureGroupRef.current,
                        }}
                    />
                    {showSuitableAreaWithoutbuilding && suitableAreaWithoutbuilding.map((data, index) => (
                        <GeoJSON key={index} data={data} style={{ color: 'green' }} />
                    ))}
                    {showSuitableArea && suitableArea.map((data, index) => (
                        <GeoJSON key={index} data={data} style={{ color: 'blue' }} />
                    ))}
                    {showBuilding && building.map((data, index) => (
                        <GeoJSON key={index} data={data} style={{ color: 'red' }} />
                    ))}
                </FeatureGroup>
            </MapContainer>

            {/* Render the legend */}
            {showLegend && <MapLegend />}
        </div>
    );
};

export default MapComponent;
