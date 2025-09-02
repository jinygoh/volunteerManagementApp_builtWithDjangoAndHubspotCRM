from locust import HttpUser, task, between
from faker import Faker

# Initialize a Faker instance for generating random test data
fake = Faker()

class VolunteerSignupUser(HttpUser):
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)

    # This host will be used if no --host is specified on the command line
    # The Django server runs on port 8000 by default.
    host = "http://127.0.0.1:8000"

    @task
    def signup_volunteer(self):
        """
        Simulates a user signing up as a volunteer.
        """
        # Generate unique user data for each request
        unique_email = f"locust_{fake.user_name()}{fake.pyint()}@example.com"

        payload = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": unique_email,
            "phone_number": fake.numerify(text='##########'),
            "preferred_volunteer_role": "Event Staff",
            "availability": "Weekends",
            "how_did_you_hear_about_us": "From a friend"
        }

        self.client.post(
            "/api/signup/",
            json=payload,
            name="/api/signup/" # Group all signup requests under this name in the stats
        )
