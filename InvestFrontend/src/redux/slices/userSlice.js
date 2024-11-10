// redux/slices/userSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  isAuthenticated: false,
  userInfo: null, // New field for storing user information
  error: null, // Field for storing error messages
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    loginSuccess: (state, action) => {
      state.isAuthenticated = true;
      state.userInfo = action.payload;
      state.error = null;
    },
    loginFailure: (state, action) => {
      state.isAuthenticated = false;
      state.userInfo = null;
      state.error = action.payload;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.userInfo = null;
    },
  },
});

export const { loginSuccess, loginFailure, logout } = userSlice.actions;
export default userSlice.reducer;
