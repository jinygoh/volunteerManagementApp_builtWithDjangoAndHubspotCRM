import React, { createContext, useState, useContext } from 'react';
import { login as apiLogin } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null);
  const navigate = useNavigate();

  const login = async (credentials) => {
    const response = await apiLogin(credentials);
    const data = response.data;
    setAuthTokens(data);
    setUser(jwtDecode(data.access));
    localStorage.setItem('authTokens', JSON.stringify(data));
    navigate('/admin/dashboard');
  };

  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  const refreshToken = async () => {
    try {
        const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
        const data = response.data;
        setAuthTokens(data);
        setUser(jwtDecode(data.access));
        localStorage.setItem('authTokens', JSON.stringify(data));
        return data;
    } catch (error) {
        console.error("Failed to refresh token", error);
        logout(); // Logout user if refresh fails
    }
  };

  const value = { user, login, logout, refreshToken, authTokens };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  return useContext(AuthContext);
};
