/**
 * @file ProtectedRoute.jsx
 * @description A component that wraps protected routes in the application.
 *
 * This component checks if a user is authenticated by using the `useAuth` hook.
 * - If the user is authenticated, it renders the child routes using the `<Outlet />` component from `react-router-dom`.
 * - If the user is not authenticated, it redirects them to the `/login` page.
 *
 * This component is used in `App.jsx` to protect admin-only sections of the site.
 */
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = () => {
  const { user } = useAuth();

  // If there's no authenticated user, redirect to the login page.
  // The `replace` prop is used to replace the current entry in the history stack,
  // so the user can't click "back" to get to the protected page after logging in.
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // If the user is authenticated, render the nested routes (e.g., the admin dashboard).
  return <Outlet />;
};

export default ProtectedRoute;
