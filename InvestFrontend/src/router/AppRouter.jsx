import React, { useEffect, Suspense, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { loginSuccess, logout } from '../redux/slices/userSlice';
import Loader from '../component/Loader'; // A fallback loader component
import usePageTitle from '../utility/usePageTitle';

// Lazy load the components
const Home = React.lazy(() => import('../pages/Home'));
const LoginPage = React.lazy(() => import('../pages/Login'));
const SignupPage = React.lazy(() => import('../pages/Signup'));
const Dashboard = React.lazy(() => import('../pages/Dashboard'));

const AppRouter = () => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  // Title map for page titles
  const titleMap = {
    '/home': 'Invest Now - Home',
    '/dashboard': 'Invest Now - Dashboard',
    '/login': 'Invest Now - Login',
    '/signup': 'Invest Now - Register',
  };

  // Check authentication state and set loading state
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const parsedData = JSON.parse(userData);
      dispatch(loginSuccess(parsedData));
    } else {
      dispatch(logout());
      localStorage.removeItem('user');
    }
    setLoading(false);
  }, [dispatch]);

  const isAuthenticated = useSelector((state) => state.user.isAuthenticated);

  // Show loader while initializing the app
  if (loading) {
    return <Loader />;
  }

  return (
    <Router>
      {/* Call the usePageTitle hook inside the Router */}
      <PageTitleWrapper titleMap={titleMap} />
      <Suspense fallback={<Loader />}>
        <Routes>
          <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage />} />
          <Route path="/signup" element={isAuthenticated ? <Navigate to="/dashboard" /> : <SignupPage />} />
          <Route path="/home" element={<Home />} />
          <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
        </Routes>
      </Suspense>
    </Router>
  );
};

// Separate component to handle page title
const PageTitleWrapper = ({ titleMap }) => {
  usePageTitle(titleMap);
  return null; // This component only changes the page title and doesn't render anything
};

export default AppRouter;
