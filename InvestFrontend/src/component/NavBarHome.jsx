import React from 'react';
import '../style/navbarhome.css';
import logo from '../assets/images/logo.png' 
import { Link } from 'react-router-dom';
const NavbarHome = () => {
    return (
        <nav className="navbar"> 
        <Link to="/home">
            <img src={logo} alt="Logo" className="logo" />        
          </Link> 
        </nav>
    );
};

export default NavbarHome;
