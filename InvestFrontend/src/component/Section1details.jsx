import React from 'react';
import '../style/section1.css'

const Section1 = () => {
    return (
        <section className="section2">
            <div className="images-container">
                <div className="image image1"></div>
                <div className="image image2"></div>
                <div className="image image3"></div>
                <div className="image image4"></div>
            </div>
            <div className="text-container">
                <h2>Criteria for Finding Suitable Areas to Build Hotels</h2>
                <p className='item'>Proximity to parks and green spaces</p>
                <p className='item'>Adequate distance from medical facilities (clinics, hospitals)</p>
                <p className='item'>Close to popular restaurants and dining establishments</p>
                <p className='item'>Within reach of essential services such as banks and ATMs</p>
                <p className='item'>Near existing entertainment venues like clubs and attractions</p>
                
                <p className='conclusion'>
                    Our criteria focus on both the accessibility of services and the potential for guest satisfaction, ensuring a balanced approach to site selection.
                </p>
            </div>
        </section>
    );
};

export default Section1;