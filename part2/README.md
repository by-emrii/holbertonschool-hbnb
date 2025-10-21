# 🏠 Holberton School - HBnB Project Part 2
HBnB is a simplified clone of the Airbnb platform. It’s designed to teach the fundamentals of back-end development, RESTful API design, and modular architecture using Python and Flask.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Architecture Overview](#business-logic-layer---architecture)
5. [API Endpoints](#-api-endpoints)
6. [Example User Endpoints](#-user-endpoints-example-)
7. [Testing](#testing)  
   - [🧪 Running Tests](#running-tests)  
   - [🧾 Documenting the Testing Process](#documenting-the-testing-process)  

## Project Structure
```
holbertonschool-hbnb/
├── app/                                # Main application package
│   │
│   ├── api/                            # API layer – handles HTTP routes and endpoints
│   │   └── v1/                         # Version 1 of the API
│   │       ├── __init__.py             # Initializes the API and namespaces
│   │       ├── amenities.py            # Endpoints for Amenity operations
│   │       ├── base_model.py           # Shared structure or base for API models
│   │       ├── places.py               # Endpoints for Place operations
│   │       ├── reservations.py         # Endpoints for Reservation operations
│   │       ├── reviews.py              # Endpoints for Review operations
│   │       └── users.py                # Endpoints for User operations
│   │
│   ├── models/                         # Data models that represent entities
│   │   ├── __init__.py                 # Initializes the models package
│   │   ├── amenity.py                  # Amenity model definition
│   │   ├── base_model.py               # Base class with shared attributes/methods
│   │   ├── place.py                    # Place model definition
│   │   ├── reservation.py              # Reservation model definition
│   │   ├── review.py                   # Review model definition
│   │   └── user.py                     # User model definition
│   │
│   ├── persistence/                    # Handles database logic
│   │   ├── __init__.py
│   │   └── repository.py               # Repository layer for CRUD operations and data storage
│   │
│   ├── services/                       # Business logic layer
│   │   ├── __init__.py
│   │   ├── amenity_service.py          # Logic for managing amenities
│   │   ├── facade.py                   # Facade pattern – simplifies API-to-service interaction
│   │   ├── place_service.py            # Logic for managing places
│   │   ├── reservation_service.py      # Logic for managing reservations
│   │   ├── review_service.py           # Logic for managing reviews
│   │   └── user_service.py             # Logic for managing users
│   │
│   └── tests/                          # Unit and integration tests
│       ├── __init__.py
│       ├── test_amenity_endpoints.py
│       ├── test_models.py              # Testing for each models
│       ├── test_place_endpoints.py
│       ├── test_reservation_endpoints.py
│       └── test_user_endpoints.py
│
├── docs/                               # Project documentation and testing reports
│   ├── user_tests.pdf                  # Documented test log for User endpoints
│   ├── place_tests.pdf                 # Documented test log for Place endpoints
│   ├── amenity_tests.pdf               # Documented test log for Amenity endpoints
│   ├── review_tests.pdf                # Documented test log for Review endpoints
│   └── reservation_tests.pdf           # Documented test log for Reservation endpoints
│
├── .gitignore                          # Specifies which files/folders Git should ignore
├── config.py                           # Configuration settings (DB, environment, etc.)
├── requirements.txt                    # Lists all Python dependencies
├── run.py                              # Entry point to start the Flask application
├── README.md                           # Project documentation
└── LICENSE                             # License information for project usage
```

## Requirements

- Python 3.x
- Flask
- Flask-RESTX

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/by-emrii/holbertonschool-hbnb.git
   cd holbertonschool-hbnb
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd part2
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```
   The API will start at:
   ```bash
   http://127.0.0.1:5000/api/v1/
   ```

## Business Logic Layer - Architecture
### Architecture Overview
1. API Layer - Presentation Layer
2. **Facade - Business Logic Layer**
3. **Services - Business Logic Layer**
4. **Models - Business Logic Layer**
5. Repository - Persistence Layer

The Business Logic Layer is organized into three main components - each component plays a distinct role in managing and orchestrating the application’s logic.

### Key Components of the Business Logic Layer:
#### 1. Facade
   The HBnBFacade class acts as a single entry point to all business operations within the application. It simplifies communication between the Presentation Layer (API
   endpoints) and the underlying Services, shielding the API from implementation details. It also ensures consistent data handling across services (via InMemoryRepository)
   
   **Example usage:**
   ```
   from app.persistence.repository import InMemoryRepository
   from app.services.user_service import UserService

   class HBnBFacade:
       def __init__(self):
           # shared repo
            self.user_repo = InMemoryRepository()

           # services using shared repos
            self.user_service = UserService(self.user_repo)
        
    """ User CRU """
    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        return self.user_service.create_user(user_data)
   ```
#### 2. Service Models
Each Service model encapsulates the business rules and logic for a specific entity (User, Place, Review, Amenity, Reservation).

   | Service           | Responsibility                                      |
   |------------------|----------------------------------------------------|
   | UserService       | Manage user creation, updates, and retrieval.     |
   | PlaceService      | Handle creation and management of property listings. |
   | AmenityService    | Manage amenities associated with places.          |
   | ReviewService     | Process user reviews and ratings for places.      |
   | ReservationService| Manage booking dates and availability logic.      |

   **Example usage:**
   ```
   from app.models.user import User
   from app.persistence.repository import InMemoryRepository

   class UserService:
       def __init__(self, user_repo):
           self.user_repo = user_repo

    # Create user
    def create_user(self, user_data):
        existing = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing:
            raise ValueError('Email already used - choose another email')
        user = User(**user_data)
        self.user_repo.add(user)
        return user
   ```
   ***Note: Part 1 currently only contains logic for CREATE, RETRIEVE and UPDATE.***

#### 3. Domain Models
Core entities representing the application’s data and simple behaviours
   | Model       | Description                       | Key Attributes                                                                 |
   |------------|-----------------------------------|-------------------------------------------------------------------------------|
   | Base       | Foundation for all entities. | id, created_at, updated_at
   | User       | Represents a HBnB platform user.  | id, first_name, last_name, email, phone_number                                |
   | Place      | Property listed for rent.          | id, user_id, title, description, price, address, latitude, longitude, image_url, amenity_ids |
   | Amenity    | Feature or facility available at a place. | id, name, description                                                      |
   | Review     | User feedback for a place.         | id, user_id, place_id, rating, comment, upload_image                          |
   | Reservation| Booking details for a place.       | id, user_id, place_id, start_date, end_date, price, discount, status, payment_status |

   **Example usage:**
   ```
   from app.models.base_model import BaseModel
   import re
   
   class User(BaseModel):
       def __init__(self, first_name, last_name, email, encrypted_password, phone_number, profile_img=None, is_admin=False):
           super().__init__()
           self.first_name = first_name
           self.last_name = last_name
           self.email = email
           self.encrypted_password = encrypted_password
           self.phone_number = phone_number
           self.profile_img = profile_img
           self.is_admin = is_admin
   
       """ Getters and Setters """
       """ First Name """
       @property
       def first_name(self):
           return self._first_name
       
       @first_name.setter
       def first_name(self, value):
           if not isinstance(value, str):
               raise TypeError("First name must be a string")
           value = value.strip()
           if len(value) < 2:
               raise ValueError("First name must be at least 2 characters")
           if len(value) >= 50:
               raise ValueError("First name cannot be more than 50 characters")
           self._first_name = value
   ```

## 🌐 API Endpoints
   ### 👥 Users ###
      1. POST /api/v1/users/  - Register a new user
      2. GET /api/v1/users/{user_id}  - Get user details
      3. PUT /api/v1/users/{user_id}  - Update user information
   ### 🏠 Places ###
      1. POST /api/v1/places/  - Create a new place
      2. GET /api/v1/places/   - Get all places 
      3. GET /api/v1/places/{place_id} - Get place details
      4. PUT /api/v1/places/{place_id}  - Update place information
   ### 📌 Amenities ###
      1. POST /api/v1/amenities/ - Create amenity
      2. GET /api/v1/amenities/ - Get all amenities
      3. GET /api/v1/amenities/{amenity_id} - Get amenity details
      4. PUT /api/v1/amenities/{amenity_id} - Update amenity
   ### 📝 Reviews ###
      1. POST /api/v1/reviews/ - Create review
      2. GET /api/v1/reviews/ - Get all reviews
      3. GET /api/v1/reviews/{review_id} - Get review details
      4. PUT /api/v1/reviews/{review_id} - Update review
      5. DELETE /api/v1/reviews/{review_id} - Delete review
   ### 🕒 Reservations ###
      1. POST /api/v1/reservations/ - Create a new reservation
      2. GET /api/v1/reservations/   - Get all reservations
      3. GET /api/v1/reservations/{reservation_id}  - Get reservation details
      4. PUT /api/v1/reservations/{reservation_id}  - Update reservation
   
## 🌐 USER Endpoints Example 🌐 ##

   ### 1. Register a New User ###
   **Endpoint** -- _POST /api/v1/users/_

   **Request Body**
   ```json
   {
     "first_name": "Alice",
     "last_name": "Smith",
     "email": "alice@example.com",
     "phone_number": "+61412345678",
     "encrypted_password": "password123"
   }
   ```
   **Response**
   ```json
   {
     "user_id": "as235bjkfas882",
     "first_name": "Alice",
     "last_name": "Smith",
     "email": "alice@example.com",
     "phone_number": "+61412345678"
   }
   ```
   ### 2. Get User Details ###
   **Endpoint** -- _GET /api/v1/users/{user_id}_

   **Example Request**
   ```
   GET /api/v1/users/as235bjkfas882
   ```
   **Response**
   ```json
   {
     "user_id": "as235bjkfas882",
     "first_name": "Alice",
     "last_name": "Smith",
     "email": "alice@example.com",
     "phone_number": "+61412345678"
   }
   ```
   ### 3. Update User Information ###
   **Endpoint** -- _PUT /api/v1/users/{user_id}_

   **Request Body**
   ```json
   {
     "first_name": "Alice",
     "last_name": "Johnson",
     "phone_number": "+61498765432"
   }
   ```
   **Response**
   ```json
   {
     "user_id": "as235bjkfas882",
     "first_name": "Alice",
     "last_name": "Johnson",
     "email": "alice@example.com",
     "phone_number": "+61412345678"
   }
   ```
   
## 🧪 Testing
### 🏃 Running Tests
Run the pytests/unittests to ensure the application is running as expected:
```
# Test models
python3 -m app.tests.test_models

# Test facade layer
python3 -m unittest app.tests.test_user_endpoints.py
python3 -m unittest app.tests.test_amenity_endpoints.py
python3 -m unittest app.tests.test_place_endpoints.py
python3 -m unittest app.tests.test_review_endpoints.py
python3 -m unittest app.tests.test_reservation_endpoints.py
```

### 🧾 Documenting the Testing Process

Each test session has been documented and saved as a PDF file for verification and presentation purposes.

For every entity, the following were recorded:

- ✅ **Endpoints tested**  
- 🧩 **Input data used**  
- 📤 **Expected output vs. actual output**  
- ⚠️ **Result**  

These files provide a detailed log of the testing process and demonstrate that the application meets all required specifications.

---

### 📚 Test Logs (click to view)

| Test Area | Description | Link |
|------------|-------------|------|
| 🧍 **User Endpoints** | Create, Retrieve, Update user tests | [View PDF](./docs/user_tests.pdf) |
| 🏠 **Place Endpoints** | Create, Retrieve, Update place tests | [View PDF](./docs/place_tests.pdf) |
| 🪩 **Amenity Endpoints** | Create, Retrieve, Update amenity tests | [View PDF](./docs/amenity_tests.pdf) |
| 💬 **Review Endpoints** | Create, Retrieve, Update, Delete review tests | [View PDF](./docs/review_tests.pdf) |
| 📅 **Reservation Endpoints** | Create, Retrieve, Update reservation tests | [View PDF](./docs/reservation_tests.pdf) |

<br>

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.
