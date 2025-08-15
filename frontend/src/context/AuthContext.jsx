import React, { createContext, useState, useContext } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/api';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async (credentials) => {
    try {
      const response = await apiLogin(credentials);
      setUser({ username: response.data.user });
      navigate('/admin/dashboard'); // Redirect to dashboard after login
    } catch (error) {
      console.error('Login failed', error);
      throw error; // Re-throw error to be caught by the login page
    }
  };

  const logout = async () => {
    try {
        await apiLogout();
    } catch (error) {
        console.error('Logout failed on server, logging out on client anyway.', error);
    } finally {
        setUser(null);
        navigate('/login');
    }
  };

  const value = { user, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
