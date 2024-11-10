import React from 'react';
import NavbarHome from '../component/NavBarHome';
import SignUpComponent from '../component/Auth/SignUpComponent';
import Footer from '../component/footer'
const SignupPage = () => {
    return (
        <>
            <NavbarHome></NavbarHome>
            <SignUpComponent></SignUpComponent>
            <Footer></Footer>
        </>
    );
};

export default SignupPage;
