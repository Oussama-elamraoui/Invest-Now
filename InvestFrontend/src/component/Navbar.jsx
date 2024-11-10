import React, { useState,useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../redux/slices/userSlice'; // Adjust the path to your logout action
import { FaUser, FaHistory, FaSignOutAlt } from 'react-icons/fa'; // Import icons
import { Link } from 'react-router-dom';
import '../style/navbar.css';
import userImage from '../assets/user.png';
import logo from '../assets/images/logo.png';

const Navbar = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const userData = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };
  useEffect(() => {
    window.dispatchEvent(new Event('resize')); // Trigger a resize to recalculate the layout
  }, []);

  const handleLogout = () => {
    setModalOpen(true);
  };

  const confirmLogout = () => {
    dispatch(logout());
    localStorage.removeItem('user');
    window.location.href = '/'; // Redirect to home after logout
  };

  return (
    <>
      <div className='navbar'>
        <div className='navbar-logo'>
          <Link to="/home">
            <img src={logo} className='logo' alt='Logo' />
          </Link>
        </div>
        <div className='navbar-user' onClick={toggleDropdown}>
          <span className='navbar-username'>{userData.userInfo.user.name}</span>
          <img src={userImage} alt='User' className='navbar-user-image' />
          {dropdownOpen && (
            <div className='navbar-dropdown'>
              <div className='navbar-dropdown-item'>
                <FaUser className='dropdown-icon' /> {userData.userInfo.user.name}
              </div>
              <div className='navbar-dropdown-item'>
                <FaHistory className='dropdown-icon' /> History
              </div>
              <div className='navbar-dropdown-item' onClick={handleLogout}>
                <FaSignOutAlt className='dropdown-icon' /> Logout
              </div>
            </div>
          )}
        </div>
      </div>
      <div className='navbar-space'></div>

      {modalOpen && (
        <div className='modal-overlay'>
          <div className='modal'>
            <h2>Confirm Logout</h2>
            <p>Are you sure you want to log out?</p>
            <div className='modal-buttons'>
              <button className='btn-confirm' onClick={confirmLogout}>
                Yes
              </button>
              <button className='btn-cancel' onClick={() => setModalOpen(false)}>
                No
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;
