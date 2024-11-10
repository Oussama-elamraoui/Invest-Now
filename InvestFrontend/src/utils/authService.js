// utils/authService.js
import axios from 'axios';
import { loginSuccess, loginFailure } from '../redux/slices/userSlice';


const API_URL = 'http://127.0.0.1:8000/api'; // Replace with your API base URL

export const login = async (credentials, dispatch) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, credentials);
    const { data } = response;
    localStorage.setItem('user', JSON.stringify(data)); // Store user data in local storage
    dispatch(loginSuccess(data)); // Dispatch success action with user data
    return true
  } catch (error) {
    const errorMessage = error.response ? error.response.data.message : 'Login failed';
    dispatch(loginFailure(errorMessage)); // Dispatch failure action with error message
    return false
  }
};

export const verifyToken = async (accessToken) => {
  console.log('my token:',accessToken)
  try {
    // const response = await axios.post(`${API_URL}/check-session/`, {
    //   token: accessToken,
    // });
    if (!accessToken) {
      return false;
  }
    const response = await axios.get(`${API_URL}/check-session/`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    return true;
  } catch (error) {
    console.error('Token verification failed:', error);
    return false;
  }
};

export const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/signup`, userData);
  return response.data;
};

export const logout = (dispatch) => {
  localStorage.removeItem('user'); // Remove user data from local storage
  dispatch(logout()); // Dispatch logout action
};
