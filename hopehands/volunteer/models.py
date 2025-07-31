from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    preferred_volunteer_role = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    lifecyclestage = models.CharField(max_length=50, default='Lead')

    def __str__(self):
        return self.name
