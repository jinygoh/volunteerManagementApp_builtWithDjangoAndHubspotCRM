from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    preferred_volunteer_role = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    how_did_you_hear_about_us = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
