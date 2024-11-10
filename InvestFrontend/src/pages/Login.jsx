import React from 'react';
import LoginComponent from '../component/Auth/LoginComponent'
import NavbarHome from '../component/NavBarHome'
import Footer from '../component/footer'
const LoginPage = () => {
  return (<>
  <NavbarHome></NavbarHome>
  <LoginComponent ></LoginComponent >
  <Footer></Footer>
  </>);
};

export default LoginPage;
