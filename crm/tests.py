from django.test import TestCase
from django.urls import reverse
from .models import Volunteer

class VolunteerModelTest(TestCase):
    def test_str_representation(self):
        volunteer = Volunteer(first_name="John", last_name="Doe")
        self.assertEqual(str(volunteer), "John Doe")

from django.contrib.auth.models import User

class VolunteerRegistrationTest(TestCase):
    def test_registration_form_renders(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/register.html')

    def test_registration_creates_volunteer(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Volunteer.objects.filter(email='jane.doe@example.com').exists())

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('volunteer_list'))
        self.assertRedirects(response, '/accounts/login/?next=/crm/')

    def test_authenticated_user_can_access_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('volunteer_list'))
        self.assertEqual(response.status_code, 200)

class ApprovalWorkflowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.approved_volunteer = Volunteer.objects.create(first_name="Approved", last_name="Volunteer", email="approved@test.com", approved=True)
        self.unapproved_volunteer = Volunteer.objects.create(first_name="Unapproved", last_name="Volunteer", email="unapproved@test.com", approved=False)

    def test_pending_volunteers_view(self):
        response = self.client.get(reverse('pending_volunteers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.unapproved_volunteer.first_name)
        self.assertNotContains(response, self.approved_volunteer.first_name)

    def test_approve_volunteer_view(self):
        response = self.client.post(reverse('approve_volunteer', args=[self.unapproved_volunteer.pk]))
        self.assertRedirects(response, reverse('pending_volunteers'))
        self.unapproved_volunteer.refresh_from_db()
        self.assertTrue(self.unapproved_volunteer.approved)

    def test_reject_volunteer_view(self):
        response = self.client.post(reverse('reject_volunteer', args=[self.unapproved_volunteer.pk]))
        self.assertRedirects(response, reverse('pending_volunteers'))
        self.assertFalse(Volunteer.objects.filter(pk=self.unapproved_volunteer.pk).exists())
