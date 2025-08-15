import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = () => {
  const { user } = useAuth();

  // If there's no user, redirect to the login page.
  // The `replace` prop is used to replace the current entry in the history stack,
  // so the user can't click "back" to get to the protected page.
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // If the user is authenticated, render the nested routes.
  return <Outlet />;
};

export default ProtectedRoute;
