// component/Auth/LoginComponent.jsx
import React, { useState } from 'react';

import { useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import { login } from '../../utils/authService'; // Import the login function
import './Auth.css';
import logo from '../../assets/images/logo.png';
import MySVGComponent from '../../assets/images/signinsvg.jsx';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';

const LoginComponent = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        const credentials = { email, password };
        login(credentials, dispatch)
        .then((res)=>{console.log(res)
          if(res){
            navigate('/dashboard')
          }
        })
        .catch((err) => setError(err.message));
    };

    return (
        <div className="auth-container">
            <div className='sub-container'>
                <div className="auth-form">
                    <img src={logo} width={'200'} style={{marginBottom:'20px'}} alt="Logo" />
                    <h2>Welcome Back!</h2>
                    <form onSubmit={handleLogin}>
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            placeholder="Enter your email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />

                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Enter your password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        {error && <p className="error">{error}</p>} {/* Display error message */}

                        <button type="submit">Login</button>
                    </form>
                    <p>
                        Don't have an account? <Link to="/signup">Sign Up</Link>
                    </p>
                </div>
                <div className="auth-image">
                    <MySVGComponent className="svg-image" />
                </div>
            </div>
        </div>
    );
};

export default LoginComponent;
