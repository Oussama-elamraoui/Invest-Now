import React from 'react';
import Lottie from 'react-lottie';
import animationData from '../assets/animation/htzSu7K0A2.json';
import { Link } from 'react-router-dom';
import '../style/getStartedSection.css';
import '../style/button.scss'

const SectionGetStarted = () => {
    const defaultOptions = {
        loop: false,
        autoplay: true,
        animationData: animationData,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };

    return (
        <section className="section1">
            <div className="text-container">
                <h1>Invest Now!</h1>
                <p>Find the perfect spot to build your hotel. Simply draw a region on the map, and we'll analyze it using advanced tools to recommend the most suitable areas for your investment.</p>
                <Link to="/login">
                <button className="button-get-started">Get Started</button></Link>
            </div>
            <div className="lottie-container">
                <Lottie options={defaultOptions} height={400} width={580} />
            </div>
        </section>
    );
};

export default SectionGetStarted;
