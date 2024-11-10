import React from 'react';
import { MapContainer, TileLayer, GeoJSON , Marker,Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { LatLngBounds } from 'leaflet';
import 'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css';
import L from 'leaflet';
import 'leaflet-extra-markers';

const GeoDataDisplay = ({ data, title, text, color, typeData,center}) => {
    const { buffer, geojson, original_points, count } = data;
    // const getCenter = (geojson) => {
    //     const bounds = new LatLngBounds();
    //     geojson.features.forEach((feature) => {
    //         const coordinates = feature.geometry.coordinates[0];
    //         coordinates.forEach((coord) => {
    //             bounds.extend([coord[1], coord[0]]);
    //         });
    //     });
    //     return bounds.getCenter();
    // };

    // const center = getCenter(geojson);
    const style = {
        mapContainer: {
            width: '600px',
            height: '400px',
            border: '1px solid #ccc',
            borderRadius: '8px',
            overflow: 'hidden',
            marginTop: '20px'
        },
        container: {
            padding: '20px',
            fontFamily: 'Arial, sans-serif'
        },
        mapWrapper: {
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            width: '100%'
        },
        title: {
            fontSize: '24px',
            fontWeight: 'bold',
            marginBottom: '10px'
        },
        text: {
            fontSize: '16px',
            marginBottom: '10px',
            color:'black'
        },
        criteria: {
            fontSize: '14px',
            marginBottom: '10px',
            color: '#555'
        }
    };
    const markerIcons = {
        red: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'red',
            shape: 'circle',
            prefix: 'fa',
        }),
        blue: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'blue',
            shape: 'circle',
            prefix: 'fa',
        }),
        green: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'green',
            shape: 'circle',
            prefix: 'fa',
        }),
        orange: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'orange',
            shape: 'circle',
            prefix: 'fa',
        }),
        purple: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'purple',
            shape: 'circle',
            prefix: 'fa',
        }),
        yellow: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'yellow',
            shape: 'circle',
            prefix: 'fa',
        }),
        cyan: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'cyan',
            shape: 'circle',
            prefix: 'fa',
        }),
        pink: L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: 'pink',
            shape: 'circle',
            prefix: 'fa',
        }),
    };

    return (
        <div style={style.container}>
            {title && <div style={style.title} className='modal-subtitle'>{title}</div>}
            <hr className="modal-separator" />
            {text && <div style={style.text}>{text}</div>}
            {buffer && <div style={style.criteria}>Buffer: {buffer}</div>}
            {count && <div style={style.criteria}>Number total of {typeData} in your region : {count}</div>}
            <div style={style.mapWrapper}>
                <div style={style.mapContainer}>
                    <MapContainer center={[center.lat, center.lon]} zoom={13} style={{ width: '100%', height: '100%' }}>
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        />
                        {geojson && (
                            <GeoJSON
                                data={geojson}
                                style={color ? { color: color } : { color: 'orange' }}
                            />
                        )}
                        {original_points && original_points.map((point, index) => (
                    <Marker key={index} position={[point.lat, point.lon]} icon={markerIcons.purple}>
                        <Popup>
                            Lat: {point.lat}, Lon: {point.lon}
                        </Popup>
                    </Marker>))}
                    </MapContainer>
                </div>
            </div>
        </div>
    );
};

export default GeoDataDisplay;
