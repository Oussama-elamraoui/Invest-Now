import React from 'react';
import '../style/loader.css'; // Add your loader styles here
import logo from '../assets/images/logo.png'; // Adjust the path to your logo

const Loader = () => {
  return (
    <div className="loader-container">
      <img src={logo} alt="Logo" className="loader-logo" />
    </div>
  );
};

export default Loader;
