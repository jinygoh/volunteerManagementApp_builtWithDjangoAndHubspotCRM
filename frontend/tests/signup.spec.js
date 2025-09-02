import { test, expect } from '@playwright/test';

test.describe('Volunteer Signup Page', () => {
  test('should allow a user to sign up successfully', async ({ page }) => {
    // Navigate to the signup page
    // The base URL is configured in playwright.config.js (or defaults to the dev server URL)
    await page.goto('/signup');

    // Check that the heading is correct
    await expect(page.getByRole('heading', { name: 'Volunteer Signup' })).toBeVisible();

    // Fill out the form
    await page.getByLabel('First Name').fill('E2E');
    await page.getByLabel('Last Name').fill('Tester');
    await page.getByLabel('Email').fill(`e2e-tester-${Date.now()}@example.com`);
    await page.getByLabel('Phone Number').fill('1234567890');
    await page.getByLabel('Preferred Volunteer Role').fill('Testing');
    await page.getByLabel('Availability').fill('All the time');
    await page.getByLabel('How did you hear about us?').fill('The Internet');

    // Click the sign-up button
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Assert that the success message is shown
    await expect(page.getByText('Thank you for signing up! Your application will be reviewed.')).toBeVisible();

    // Optional: Assert that the form has been cleared
    await expect(page.getByLabel('First Name')).toBeEmpty();
  });
});
