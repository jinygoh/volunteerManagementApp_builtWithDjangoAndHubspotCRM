# Django Backend Crash Course

This guide provides a crash course on the key components of the Django backend for the HopeHands application.

## 1. The Model-View-Template (MVT) Pattern... and APIs

Traditionally, Django uses the Model-View-Template pattern. However, in this project, we are using Django to build a **REST API**, so the "Template" part is replaced by our **React frontend**. The pattern for our backend is closer to:

**Model -> View -> Serializer**

-   **Model:** Defines the structure of our data (the database schema).
-   **View:** Handles incoming HTTP requests and implements the business logic.
-   **Serializer:** Converts our complex data (like model instances) into a format that can be easily sent over the internet (JSON).

## 2. The `Volunteer` Model

The heart of our application's data is the `Volunteer` model.

**File:** `hopehands/volunteer/models.py`

```python
class Volunteer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    # ... other fields ...

    # Used in the admin approval workflow.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # Stores the HubSpot Contact ID after a volunteer is approved and synced.
    hubspot_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
```

### Key Concepts:

-   **`models.Model`**: Every model is a Python class that subclasses `django.db.models.Model`.
-   **Fields**: Each attribute of the model represents a database field (e.g., `name = models.CharField(...)` creates a `VARCHAR` column in the database).
-   **`status` field**: This is the most important field for our business logic. The `choices` option provides a dropdown in the Django admin, and `default='pending'` ensures all new volunteers start in the correct state.
-   **Migrations**: Whenever you change this `models.py` file, you must run `python hopehands/manage.py makemigrations` and `python hopehands/manage.py migrate` to update the database schema.

## 3. The API Views

The views are where the main logic lives. We use **Django REST Framework (DRF)** to build our views.

**File:** `hopehands/volunteer/api_views.py`

### `VolunteerViewSet`

This is the main view for administrators.

```python
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all().order_by('-id')
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]
```

-   **`viewsets.ModelViewSet`**: This is a powerful class from DRF that automatically provides the standard `list()`, `create()`, `retrieve()`, `update()`, and `destroy()` actions for a model.
-   **`queryset`**: This defines the set of objects that this view will operate on (all `Volunteer` objects).
-   **`serializer_class`**: This tells the view to use our `VolunteerSerializer` to convert the data.
-   **`permission_classes`**: This is crucial for security. `[IsAuthenticated]` means that only logged-in users can access any of the actions in this viewset.

### Custom Actions: `approve` and `reject`

DRF allows us to add our own custom actions to a viewset.

```python
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        # ... logic to approve a volunteer ...
```

-   **`@action(...)`**: This decorator registers a new route.
-   **`detail=True`**: This means the action operates on a single instance of a model (a detail view). The URL will be `/api/volunteers/{id}/approve/`.
-   **`methods=['post']`**: This action only responds to `POST` requests.
-   **Inside the method**: We get the volunteer object (`self.get_object()`), change its status, call the HubSpot API, and save the object. This is the core of the approval workflow.

## 4. URL Routing

The final piece is connecting a URL to a view.

**File:** `hopehands/volunteer/api_urls.py`

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'volunteers', api_views.VolunteerViewSet, basename='volunteer')

urlpatterns = [
    path('', include(router.urls)),
]
```

-   **`DefaultRouter`**: DRF's router automatically generates all the standard URLs for our `VolunteerViewSet`. For example, it creates:
    -   `GET /api/volunteers/` (for the list)
    -   `POST /api/volunteers/` (for creating)
    -   `GET /api/volunteers/{id}/` (for retrieving one)
    -   `PUT /api/volunteers/{id}/` (for updating)
    -   And it also automatically creates the URLs for our custom actions, like `POST /api/volunteers/{id}/approve/`.

This setup provides a powerful and secure backend API with minimal code, allowing us to focus on the core business logic of the application.
