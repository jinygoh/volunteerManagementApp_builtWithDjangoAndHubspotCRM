from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Volunteer
from unittest.mock import patch

class VolunteerModelTests(TestCase):
    def test_can_create_multiple_volunteers_with_null_hubspot_id(self):
        """
        Tests that multiple volunteers can be created with hubspot_id=None
        without violating any unique constraints.
        """
        try:
            Volunteer.objects.create(
                first_name='Test',
                last_name='User1',
                email='test1@example.com',
                phone_number='1234567890'
            )
            Volunteer.objects.create(
                first_name='Test',
                last_name='User2',
                email='test2@example.com',
                phone_number='0987654321'
            )
        except Exception as e:
            self.fail(f"Creating multiple volunteers with null hubspot_id failed: {e}")

        self.assertEqual(Volunteer.objects.count(), 2)


class VolunteerAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'apiuser'
        self.password = 'apipass'
        self.user = User.objects.create_user(username=self.username, password=self.password, is_staff=True)
        self.volunteer_data = {
            'first_name': 'API Test',
            'last_name': 'Volunteer',
            'email': 'apitest@example.com',
            'phone_number': '9876543210',
            'preferred_volunteer_role': 'Test Role',
            'availability': 'Weekends'
        }
        self.signup_url = reverse('volunteer-signup-api')
        self.volunteers_url = reverse('volunteer-list')

    def test_public_signup_api(self):
        """
        Tests that the public signup API endpoint creates a new volunteer.
        """
        response = self.client.post(self.signup_url, self.volunteer_data, format='json')
        self.assertEqual(response.status_code, 201, response.content) # 201 Created
        self.assertEqual(Volunteer.objects.count(), 1)
        self.assertEqual(Volunteer.objects.get().first_name, 'API Test')
        self.assertEqual(Volunteer.objects.get().status, 'pending')

    def test_volunteer_api_unauthenticated_access(self):
        """
        Tests that unauthenticated users cannot access the main volunteer API.
        """
        response = self.client.get(self.volunteers_url)
        self.assertEqual(response.status_code, 401) # 401 Unauthorized

    def test_volunteer_api_authenticated_access(self):
        """
        Tests that an authenticated user can list volunteers via the API.
        """
        # Create a volunteer first
        Volunteer.objects.create(**self.volunteer_data)
        # Obtain a token
        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']
        # Make the request with the token
        response = self.client.get(self.volunteers_url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], self.volunteer_data['first_name'])

    @patch('volunteer.api_views.HubspotAPI')
    def test_approve_action(self, MockHubspotAPI):
        """
        Tests the custom 'approve' action on the ViewSet, mocking the HubSpot API call.
        """
        # Configure the mock to simulate a successful API call
        mock_hubspot_instance = MockHubspotAPI.return_value
        mock_hubspot_instance.create_contact.return_value.id = 'hs_12345'

        volunteer = Volunteer.objects.create(**self.volunteer_data)
        approve_url = reverse('volunteer-approve', kwargs={'pk': volunteer.pk})

        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']
        response = self.client.post(approve_url, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)

        # Refresh the volunteer from the database to get the updated status
        volunteer.refresh_from_db()
        self.assertEqual(volunteer.status, 'approved')
        self.assertEqual(volunteer.hubspot_id, 'hs_12345')

        # Verify that the mocked API was called with the correct arguments
        mock_hubspot_instance.create_contact.assert_called_once_with(
            email=volunteer.email,
            first_name=volunteer.first_name,
            last_name=volunteer.last_name,
            phone_number=volunteer.phone_number,
            preferred_volunteer_role=volunteer.preferred_volunteer_role,
            availability=volunteer.availability,
            how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
        )
