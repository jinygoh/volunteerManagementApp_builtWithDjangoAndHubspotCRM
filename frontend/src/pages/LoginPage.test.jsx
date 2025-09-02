import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LoginPage from './LoginPage';
import { AuthContext } from '../context/AuthContext';
import { MemoryRouter } from 'react-router-dom';

// Mock the AuthContext
const mockAuthContext = {
  login: vi.fn(),
  user: null,
};

describe('LoginPage', () => {
  it('renders the login form correctly', () => {
    render(
      <MemoryRouter>
        <AuthContext.Provider value={mockAuthContext}>
          <LoginPage />
        </AuthContext.Provider>
      </MemoryRouter>
    );

    // Check for the main heading
    expect(screen.getByRole('heading', { name: /admin login/i })).toBeInTheDocument();

    // Check for form elements
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });
});
