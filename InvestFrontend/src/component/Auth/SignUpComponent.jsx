import React from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';
import logo from '../../assets/images/logo.png'
import MySVGComponent from '../../assets/images/signupsvg.jsx'; 

const SignUpComponent = () => {
    return (
        <div className="auth-container">
            <div className='sub-container'>
            <div className="auth-form">
                <img src={logo} width={'200'} style={{marginBottom:'20px'}}></img>
                <h2>Create Account</h2>
                <form>
                    <label htmlFor="name">Full Name</label>
                    <input type="text" id="name" placeholder="Enter your full name" required />

                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" placeholder="Enter your email" required />

                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" placeholder="Create a password" required />

                    <button type="submit">Sign Up</button>
                </form>
                <p>
                    Already have an account? <Link to="/login">Login</Link>
                </p>
            </div>
            <div className="auth-image">
                <MySVGComponent className="svg-image"></MySVGComponent>
            </div>
        </div>
        </div>
    );
};

export default SignUpComponent;
