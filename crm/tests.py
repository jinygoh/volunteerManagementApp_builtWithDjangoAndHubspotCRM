from django.test import TestCase
from django.urls import reverse
from .models import Volunteer

class VolunteerModelTest(TestCase):
    def test_str_representation(self):
        volunteer = Volunteer(first_name="John", last_name="Doe")
        self.assertEqual(str(volunteer), "John Doe")

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
