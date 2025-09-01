import io
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Volunteer
from unittest.mock import patch


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

    def test_approve_action(self):
        """
        Tests the custom 'approve' action on the ViewSet.
        """
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        approve_url = reverse('volunteer-approve', kwargs={'pk': volunteer.pk})

        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']
        response = self.client.post(approve_url, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)

        # Refresh the volunteer from the database to get the updated status
        volunteer.refresh_from_db()
        self.assertEqual(volunteer.status, 'approved')

    def test_reject_action(self):
        """
        Tests the custom 'reject' action on the ViewSet.
        """
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        reject_url = reverse('volunteer-reject', kwargs={'pk': volunteer.pk})

        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']
        response = self.client.post(reject_url, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)

        volunteer.refresh_from_db()
        self.assertEqual(volunteer.status, 'rejected')

    def test_delete_action(self):
        """
        Tests that an authenticated user can delete a volunteer via the API.
        """
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        self.assertEqual(Volunteer.objects.count(), 1)

        delete_url = reverse('volunteer-detail', kwargs={'pk': volunteer.pk})

        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']
        response = self.client.delete(delete_url, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 204) # 204 No Content for successful deletion
        self.assertEqual(Volunteer.objects.count(), 0)

    def test_visualization_endpoint(self):
        """
        Tests the visualization endpoint to ensure it returns aggregated data correctly.
        """
        # Create some volunteers with different roles
        Volunteer.objects.create(first_name='A', last_name='1', email='a1@test.com', preferred_volunteer_role='Food Distribution', availability='Mon')
        Volunteer.objects.create(first_name='B', last_name='2', email='b2@test.com', preferred_volunteer_role='Food Distribution', availability='Tue')
        Volunteer.objects.create(first_name='C', last_name='3', email='c3@test.com', preferred_volunteer_role='Teaching', availability='Wed')

        # Obtain a token
        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']

        # Make the request
        url = reverse('visualization-volunteer-roles')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2) # Two distinct roles

        # The response is ordered by count descending
        self.assertEqual(response.data[0]['preferred_volunteer_role'], 'Food Distribution')
        self.assertEqual(response.data[0]['count'], 2)
        self.assertEqual(response.data[1]['preferred_volunteer_role'], 'Teaching')
        self.assertEqual(response.data[1]['count'], 1)

    def test_csv_upload(self):
        """
        Tests the CSV upload functionality, ensuring volunteers are
        created and approved locally.
        """
        # Create a CSV file in memory
        csv_data = (
            "First Name,Last Name,Email,Phone Number,Preferred Volunteer Role,Availability\n"
            "CSV,User1,csv1@example.com,111,Role1,Mon\n"
            "CSV,User2,csv2@example.com,222,Role2,Tue\n"
        )
        csv_file = io.StringIO(csv_data)
        csv_file.name = 'test.csv'

        # Obtain a token
        token_response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        token = token_response.data['access']

        # Make the request
        url = reverse('upload-csv')
        response = self.client.post(url, {'file': csv_file}, HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Volunteer.objects.count(), 2)

        # Verify volunteers were created as 'approved'
        self.assertEqual(Volunteer.objects.get(email='csv1@example.com').status, 'approved')
        self.assertEqual(Volunteer.objects.get(email='csv2@example.com').status, 'approved')
