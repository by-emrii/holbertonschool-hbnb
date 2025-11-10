# 🏠 Holberton School - HBnB Project Part 3
This phase of the Holberton HBnB Project delivers a secure and database-driven backend built with Flask, SQLAlchemy, and JWT authentication.

The application now supports persistent data storage, user authentication, and role-based authorization using a scalable architecture designed for production deployment.

## Overview

Part 3 enhances the HBnB backend by integrating:

- Persistent database storage via SQLAlchemy
- JWT-based authentication and role-based access control (RBAC)
- Full CRUD operations for all entities
- Data validation and schema visualization
- Production-ready configuration supporting both SQLite (development) and MySQL (production)
This update transforms the prototype backend from an in-memory system into a robust RESTful API.

## Table of Contents
1. [Key Features](#key-features)
1. [Project Structure](#project-structure)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Architecture Overview](#business-logic-layer---architecture)
5. [API Endpoints](#-api-endpoints)
6. [Example Admin User Endpoints](#-admin-endpoints-example-)
8. [License](#-license)

## Key Features
### 🔐 Authentication and Authorization
- Secure login using JWT tokens (flask-jwt-extended)
- Password hashing with Flask-Bcrypt
- Role-based access control via the is_admin attribute
- Token-protected endpoints for all authenticated routes

### 🗄️ Database Integration
- Data persistence using SQLAlchemy ORM
- SQLite configured for local development
- MySQL ready for production deployment
- Database schema designed and visualized with mermaid.js

### ⚙️ CRUD Operations
Full CRUD functionality for:
   - Users
   - Places
   - Reviews
   - Amenities
   - Reservations
- Centralized repository and service layers for clean separation of concerns

### 🧩 Clean Architecture
- Repository layer manages database operations
- Service layer encapsulates business logic
- API layer exposes RESTful endpoints using Flask-RESTX namespaces
- Application factory pattern for modular configuration and environment handling

## Project Structure
```
holbertonschool-hbnb/part3
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
│   │       ├── users.py                # Endpoints for User operations
|   |       ├── admin.py                # Endpoints for Admin only operations
|   |       └── auth.py                 # Endpoints for Login functionality using JWT
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
│   │   ├── repository.py               # Repository layer for CRUD operations and data storage
│   │   ├── user_repository.py          # Repository layer for User specific operations
│   │   ├── amenity_repository.py       # Repository layer for Amenity specific operations
│   │   ├── place_repository.py         # Repository layer for Place specific operations
│   │   └── review_repository.py        # Repository layer for Review specific operations
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
│   ├── tests/                          # Unit and integration tests
│   |   ├── __init__.py
│   |   ├── test_amenity_endpoints.py
│   |   ├── test_models.py              # Testing for each models
│   |   ├── test_place_endpoints.py
│   |   ├── test_reservation_endpoints.py
│   |   └── test_user_endpoints.py
│   │
│   └── __init__.py                    # Initialises Flask app, extensions, and API namespaces
│   
│
│
├── docs/                               # Project documentation and testing reports
│   ├── user_tests.pdf                  # Documented test log for User endpoints
│   ├── place_tests.pdf                 # Documented test log for Place endpoints
│   ├── amenity_tests.pdf               # Documented test log for Amenity endpoints
│   ├── review_tests.pdf                # Documented test log for Review endpoints
│   └── reservation_tests.pdf           # Documented test log for Reservation endpoints
│
├── SQLScript/                          # SQL Scripts
│   └── data.sql                        # Script for table generation and initial data
|
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
   cd part3
   pip install -r requirements.txt
   ```

4. **Create Tables**
   ```bash
   flask shell
   from app import db
   db.create_all
   exit()
   ```

5. **Populate tables with initial data with SQL Script**
   ```bash
   sqlite3 instance/development.db < SQLScript/data.sql
   ```

6. **Run the application**
   ```bash
   python run.py
   ```
   The API will start at:
   ```bash
   http://127.0.0.1:5000/api/v1/
   ```


## HBnB Architecture Overview
### Architecture Overview
1. API Layer - Presentation Layer
2. Facade - Business Logic Layer
3. Services - Business Logic Layer
4. Models - Business Logic Layer
5. Repository - Persistence Layer


### Presentation Layer
The Presentation Layer manages all HTTP interactions.
It is implemented using Flask-RESTX, which provides a structured way to define endpoints, request/response models, and automatic API documentation.
Key Responsibilities:

Define API namespaces for entities such as Users, Places, Amenities, Reviews, and - Reservations
- Handle request validation, serialization, and response formatting
- Manage authentication and authorization via JWTs
- Delegate business operations to the Facade Layer

Example:
When a client sends a request to /api/v1/users, the Presentation Layer:
- Validates the input using a Flask-RESTX model
- Calls the corresponding method in the Facade
- Returns a JSON response


### Business Logic Layer
The Business Logic Layer (BLL) contains the application’s core rules and workflows.
It is composed of three main parts: the Facade, Services, and Domain Models.

#### 1. Facade Layer
The Facade acts as the bridge between the Presentation Layer and Services.
It exposes high-level operations (e.g., create_user, update_place) that internally call one or more services.

This simplifies controller code and keeps the API layer clean and uniform.

Example Flow:
```
/api/v1/users  →  Facade  →  UserService  →  UserRepository
```

#### 2. Service Layer
Each Service model encapsulates the business rules and logic for a specific entity (User, Place, Review, Amenity, Reservation).

   | Service           | Responsibility                                                            |
   |-------------------|---------------------------------------------------------------------------|
   | UserService       | Manages user creation, authentication, updates, and admin privileges.     |
   | PlaceService      | Handle creation and management of property listings.                      |
   | AmenityService    | Manage amenities associated with places.                                  |
   | ReviewService     | Process user reviews and ratings for places.                              |
   | ReservationService| Manage booking dates and availability logic.                              |

   **Example usage:**
   ```
   from app.models.user import User

   class UserService:
      def __init__(self, user_repo):
         self.user_repo = user_repo

      # Create user
      def create_user(self, user_data):
         existing = self.user_repo.get_by_attribute('email', user_data['email'])
         if existing:
               raise ValueError('Email already used - choose another email')
         user = User(**user_data)
         user.hash_password(user_data['password']) # hash pwd before saving
         self.user_repo.add(user)
         return user
   ```

#### 3. Domain Models
The Models represent core entities and their relationships, implemented using SQLAlchemy ORM.
Each model inherits from a shared BaseModel, which includes fields like id, created_at, and updated_at.

Relationships are explicitly defined between models:
- A User can own multiple Places
- A Place can have multiple Reviews
- A Place can have many Amenities (many-to-many)
- A User can make Reservations

   | Model       | Description                       | Key Attributes                                                                 |
   |------------|-----------------------------------|-------------------------------------------------------------------------------|
   | Base       | Foundation for all entities.      | id, created_at, updated_at
   | User       | Represents a HBnB platform user.  | id, first_name, last_name, email, password, phone number                              |
   | Place      | Property listed for rent.         | id, user_id, title, description, price, address, latitude, longitude, amenity_ids |
   | Amenity    | Feature or facility available at a place. | id, name, description                                                      |
   | Review     | User feedback for a place.         | id, user_id, place_id, rating, comment, upload_image                          |
   | Reservation| Booking details for a place.       | id, user_id, place_id, start_date, end_date, price, discount, status, payment_status |

   **Example usage:**
   ```
   from app import db
   from app.models.base_model import BaseModel
   from sqlalchemy.orm import validates

   class User(BaseModel):
      __tablename__ = 'users'

      first_name = db.Column(db.String(50), nullable=False)
      last_name = db.Column(db.String(50), nullable=False)
      email = db.Column(db.String(120), nullable=False, unique=True)
      password = db.Column(db.String(128), nullable=False)
      is_admin = db.Column(db.Boolean, default=False)
      phone_number = db.Column(db.String, nullable=True)
      profile_img = db.Column(db.String, nullable=True)

      places = relationship('Place', backref='owner', lazy=True)
      reviews = relationship('Review', backref='user', lazy=True)

      @validates('first_name', 'last_name')
      def validate_name(self, key, value):
         """ First and last name validations """
         if not isinstance(value, str):
               raise TypeError(f"{key.replace('_',' ').title()} must be a string")
         value = value.strip()
         if len(value) > 50:
               raise ValueError(f"{key.replace('_', ' ').title()} cannot exceed 50 characters")
         return value
   ```

## 🌐 API Endpoints
   ### 👥 Users ###
      1. GET /api/v1/users/  - Get all existing users
      2. GET /api/v1/users/{user_id}  - Get user details
   ### 🔰 Admin ###
      1. POST /api/v1/users/  - Admin can register new users
      2. PUT /api/v1/users/{user_id}  - Admin can update user information
      3. POST /api/v1/amenities/ - Admin can create amenities
      4. PUT /api/v1/amenities/{amenity_id} - Admin can update amenity
   ### 🛠️ Login ###
      1. POST /api/v1/auth/login - Any user can login with email and password
      2. GET /api/v1/auth/protected - A protected endpoint that requires JWT token
   ### 🏠 Places ###
      1. POST /api/v1/places/  - Create a new place
      2. GET /api/v1/places/   - Get all places 
      3. GET /api/v1/places/{place_id} - Get place details
      4. PUT /api/v1/places/{place_id}  - Update place information
      5. DELETE /api/v1/places/{place_id} - Delete a place
   ### 📌 Amenities ###
      1. GET /api/v1/amenities/ - Get all amenities
      2. GET /api/v1/amenities/{amenity_id} - Get amenity details
      3. DELETE /api/v1/amenities/{amenity_id} - Admin can delete any amenity
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
   
## 🌐 Admin Endpoints Example 🌐 ##

   ### 1. Register a New User ###
   **Endpoint** -- _POST /api/v1/users/_

   **Request Body**
   ```json
   {
     "first_name": "Alice",
     "last_name": "Smith",
     "email": "alice@example.com",
     "phone_number": "+61412345678",
     "password": "password123"
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


## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.
