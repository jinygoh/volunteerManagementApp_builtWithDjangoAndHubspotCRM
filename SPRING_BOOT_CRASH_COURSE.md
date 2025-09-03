# Spring Boot Backend Crash Course

This guide provides a crash course on the key components of the Spring Boot backend for the HopeHands application.

## 1. The Model-Repository-Service-Controller Pattern

Spring Boot applications often follow a layered architecture. For our REST API, the pattern is:

**Model -> Repository -> Service -> Controller**

-   **Model (JPA Entity):** Defines the structure of our data (the database schema).
-   **Repository (Spring Data JPA):** An interface that provides methods for database operations (CRUD, etc.).
-   **Service:** Contains the business logic. It uses the repository to interact with the database.
-   **Controller (REST Controller):** Handles incoming HTTP requests, calls the appropriate service methods, and returns a response.

## 2. The `Volunteer` Entity

The heart of our application's data is the `Volunteer` entity.

**File:** `backend/src/main/java/com/hopehands/model/Volunteer.java`

```java
@Entity
public class Volunteer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;

    @Column(unique = true)
    private String email;

    private String phoneNumber;
    private String preferredVolunteerRole;
    private String availability;
    private String howDidYouHearAboutUs;

    private String status;

    // Getters and Setters...
}
```

### Key Concepts:

-   **`@Entity`**: Marks this class as a JPA entity, which means it will be mapped to a table in the database.
-   **`@Id` and `@GeneratedValue`**: Specify the primary key and how it's generated.
-   **`@Column(unique = true)`**: Ensures that the email address is unique in the database.
-   **`status` field**: This is the most important field for our business logic. It will be set to "pending" by default in the service layer.

## 3. The `VolunteerRepository`

The repository is an interface that extends `JpaRepository`. Spring Data JPA automatically provides implementations for the standard CRUD methods.

**File:** `backend/src/main/java/com/hopehands/repository/VolunteerRepository.java`

```java
@Repository
public interface VolunteerRepository extends JpaRepository<Volunteer, Long> {
}
```

## 4. The `VolunteerService`

The service class contains the business logic.

**File:** `backend/src/main/java/com/hopehands/service/VolunteerService.java`

```java
@Service
public class VolunteerService {

    @Autowired
    private VolunteerRepository volunteerRepository;

    public Volunteer createVolunteer(Volunteer volunteer) {
        volunteer.setStatus("pending");
        return volunteerRepository.save(volunteer);
    }

    // other methods...
}
```

## 5. The `VolunteerController`

The controller exposes our API endpoints.

**File:** `backend/src/main/java/com/hopehands/controller/VolunteerController.java`

```java
@RestController
@RequestMapping("/api")
public class VolunteerController {

    @Autowired
    private VolunteerService volunteerService;

    @PostMapping("/signup")
    public ResponseEntity<Volunteer> signup(@RequestBody Volunteer volunteer) {
        Volunteer createdVolunteer = volunteerService.createVolunteer(volunteer);
        return new ResponseEntity<>(createdVolunteer, HttpStatus.CREATED);
    }

    @GetMapping("/volunteers")
    public List<Volunteer> getVolunteers() {
        return volunteerService.getVolunteers();
    }

    // other endpoints...
}
```

### Key Concepts:

-   **`@RestController`**: A convenience annotation that combines `@Controller` and `@ResponseBody`.
-   **`@RequestMapping("/api")`**: Sets the base path for all endpoints in this controller.
-   **`@PostMapping("/signup")`**: Maps `POST` requests for `/api/signup` to this method.
-   **`@RequestBody`**: Tells Spring to deserialize the request body into a `Volunteer` object.
-   **`ResponseEntity`**: A generic class that represents the entire HTTP response, including status code, headers, and body.
-   **`@Autowired`**: Used for dependency injection. Spring automatically injects an instance of `VolunteerService`.

This setup provides a powerful and secure backend API with minimal code, allowing us to focus on the core business logic of the application.
