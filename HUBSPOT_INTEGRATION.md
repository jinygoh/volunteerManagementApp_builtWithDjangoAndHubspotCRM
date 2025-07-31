# HubSpot Integration Instructions

To integrate with HubSpot, you will need to follow these steps:

1. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file:**
   - Create a file named `.env` in the root directory of the project.
   - Add the following lines to the `.env` file, replacing the placeholder values with your actual credentials:
     ```
     
     ```

3. **Uncomment the HubSpot integration code:**
   - Open the `hopehands/volunteer/views.py` file.
   - Uncomment the following lines:
     ```python
     # from hopehands.hubspot_api import HUBSPOT_API_KEY
     # from hubspot import HubSpot
     # from hubspot.crm.contacts import SimplePublicObjectInput
     # from hubspot.crm.contacts.exceptions import ApiException
     ```
   - Uncomment the following code block inside the `volunteer_signup` view:
     ```python
     # if form.is_valid():
     #     volunteer = form.save()
     #     try:
     #         hubspot = HubSpot(api_key=HUBSPOT_API_KEY)
     #         properties = {
     #             "email": volunteer.email,
     #             "firstname": volunteer.name,
     #             "phone": volunteer.phone_number,
     #             "lifecyclestage": "lead"
     #         }
     #         simple_public_object_input = SimplePublicObjectInput(properties=properties)
     #         api_response = hubspot.crm.contacts.basic_api.create(
     #             simple_public_object_input=simple_public_object_input
     #         )
     #         print(api_response)
     #     except ApiException as e:
     #         print("Exception when creating contact: %s\n" % e)
     #     return redirect('success')
     ```

4. **Run the development server:**
   ```bash
   python hopehands/manage.py runserver
   ```

5. **Test the integration:**
   - Go to the volunteer signup page in your browser.
   - Fill out the form and submit it.
   - Check your HubSpot account to see if the new contact was created.
