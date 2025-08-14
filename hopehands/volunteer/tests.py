from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Volunteer

class VolunteerAdminViewTests(TestCase):
    def setUp(self):
        # Create a client to make requests
        self.client = Client()
        # Create a user for logging in
        self.username = 'testadmin'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Create a sample volunteer
        self.volunteer = Volunteer.objects.create(
            name='Test Volunteer',
            email='test@example.com',
            phone_number='1234567890'
        )
        # URL for the volunteer list page
        self.volunteer_list_url = reverse('volunteer_list')

    def test_volunteer_list_redirects_if_not_logged_in(self):
        """
        Tests that accessing the volunteer list view without being logged in
        redirects to the login page.
        """
        response = self.client.get(self.volunteer_list_url)
        # Check for redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        # Check that it redirects to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={self.volunteer_list_url}")

    def test_volunteer_list_accessible_if_logged_in(self):
        """
        Tests that the volunteer list page is accessible to a logged-in user.
        """
        # Log the user in
        self.client.login(username=self.username, password=self.password)
        # Access the page
        response = self.client.get(self.volunteer_list_url)
        # Check for success (status code 200)
        self.assertEqual(response.status_code, 200)
        # Check that the volunteer's name is on the page
        self.assertContains(response, self.volunteer.name)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'volunteer/volunteer_list.html')

from unittest.mock import patch

class VolunteerAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'apiuser'
        self.password = 'apipass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.volunteer_data = {
            'name': 'API Test Volunteer',
            'email': 'apitest@example.com',
            'phone_number': '9876543210',
            'preferred_volunteer_role': 'Test Role',
            'availability': 'Weekends'
        }
        self.signup_url = reverse('volunteer-signup-api')
        self.volunteers_url = '/api/volunteers/'

    def test_public_signup_api(self):
        """
        Tests that the public signup API endpoint creates a new volunteer.
        """
        response = self.client.post(self.signup_url, self.volunteer_data, format='json')
        self.assertEqual(response.status_code, 201, response.data) # 201 Created
        self.assertEqual(Volunteer.objects.count(), 1)
        self.assertEqual(Volunteer.objects.get().name, 'API Test Volunteer')
        self.assertEqual(Volunteer.objects.get().status, 'pending')

    def test_volunteer_api_unauthenticated_access(self):
        """
        Tests that unauthenticated users cannot access the main volunteer API.
        """
        response = self.client.get(self.volunteers_url)
        self.assertEqual(response.status_code, 403) # 403 Forbidden

    def test_volunteer_api_authenticated_access(self):
        """
        Tests that an authenticated user can list volunteers via the API.
        """
        # Create a volunteer first
        Volunteer.objects.create(**self.volunteer_data)
        # Log in and make the request
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.volunteers_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.volunteer_data['name'])

    @patch('volunteer.api_views.HubspotAPI')
    def test_approve_action(self, MockHubspotAPI):
        """
        Tests the custom 'approve' action on the ViewSet, mocking the HubSpot API call.
        """
        # Configure the mock to simulate a successful API call
        mock_hubspot_instance = MockHubspotAPI.return_value
        mock_hubspot_instance.create_contact.return_value.id = 'hs_12345'

        volunteer = Volunteer.objects.create(**self.volunteer_data)
        approve_url = f'/api/volunteers/{volunteer.id}/approve/'

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(approve_url)

        self.assertEqual(response.status_code, 200)

        # Refresh the volunteer from the database to get the updated status
        volunteer.refresh_from_db()
        self.assertEqual(volunteer.status, 'approved')
        self.assertEqual(volunteer.hubspot_id, 'hs_12345')

        # Verify that the mocked API was called exactly once
        mock_hubspot_instance.create_contact.assert_called_once()
