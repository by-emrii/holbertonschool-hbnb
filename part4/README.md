# 🏠 Holberton School HBnB Project Part 4 - Simple Web Client

This project implements the frontend interface for the HBNB accommodation platform, completing Part 4 of the Holberton School full-stack series.

It connects a custom Flask API (from Part 3) with a fully functional web client built using HTML5, CSS3, and JavaScript ES6.

The frontend allows users to:

- Log in and obtain a JWT token
- View a list of places
- Filter places by price
- View detailed information about a place
- Add reviews (authenticated users only)

The frontend is designed for simplicity, responsiveness, and clean API communication.


## Project Structure

```
holbertonschool-hbnb/
│
└── part4/
    ├── backend/                         # Flask backend (API + server-side rendering) - unchanged from Part 3
    │   ├── app/
    │   │   ├── __pycache__/
    │   │   ├── api/                     # API routes
    │   │   ├── models/                  # Models
    │   │   ├── services/                # Business logic
    │   │   ├── persistence/             # Database / repository layer
    │   │   └── __init__.py              # App factory + API registration
    │   │
    │   ├── docs/                        # Backend-related documentation
    │   ├── instance/
    │   │   └── development.db           # SQLite DB
    │   │
    │   ├── SQLScript/                   # SQL setup scripts
    │   │   ├── create_database.sql
    │   │   └── run_operations.sql
    │   │
    │   ├── config.py                    # Backend configuration
    │   ├── run.py                       # Backend entry point
    │   ├── seed_data.sql                # Initial data to seed
    │   └── .gitignore
    │
    ├── frontend/
    │   ├── static/                      # Public-facing web assets
    │   │   ├── css/
    │   │   │   ├── index.css
    │   │   │   ├── login.css
    │   │   │   ├── place_details_style.css
    │   │   │   ├── review_style.css
    │   │   │   └── styles.css
    │   │   ├── fonts/
    │   │   ├── images/                  # Images to render on the website
    │   │   └── javascript/              # Frontend logic, fetch API calls, UI handlers
    │   │       ├── add_review.js
    │   │       ├── index.js
    │   │       ├── place_details.js
    │   │       └── scripts.js
    │   │
    │   ├── templates/                   # Jinja2 HTML templates
    │   │   ├── add_review/
    │   │   │   └── add_review.html
    │   │   ├── includes/
    │   │   │   ├── footer.html
    │   │   │   └── header.html          # Navbar, login/logout button, etc.
    │   │   ├── index/
    │   │   │   └── index.html           # Homepage – shows places
    │   │   ├── login/
    │   │   │   └── login.html           # Login page
    │   │   └── place_details/
    │   │       └── place_details.html   # Single place details + reviews
    │   │
    │   ├── readme.md                    # Frontend-specific README
    │   └── ER_Diagram.png               # Visual DB reference for documentation
    │
    ├── README.md                        # Main project-level README (backend + frontend)
    └── requirements.txt                 # Python dependencies

```

## Requirements

- Python 3.x
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLAlchemy
- SQLite (for development) / MySQL (for production)
- Flask-cors


## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/by-emrii/holbertonschool-hbnb.git
   cd holbertonschool-hbnb
   ```

2. **Create a virtual environment**

   > Ensure that you have python installed before running the command

   **macOS/Ubuntu**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   cd part4
   pip install -r requirements.txt
   ```

4. **Create Tables**

   ```bash
   cd backend
   flask shell
   ```

   Then inside the shell:

   ```bash
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. **Populate tables with initial data**

   > This seeds initial data such as Admin users and Regular users, Places, Amenities, and Reviews

   ```bash
   sqlite3 instance/development.db < seed_data.sql
   ```

6. **Run the application**
   ```bash
   python3 run.py
   ```
   The API will start at:
   ```bash
   http://127.0.0.1:5000/
   ```


## How to Test the Login and Add Review Functionality

The login feature is implemented on the /login page.
This page communicates with the backend authentication endpoint:

```bash
POST /api/v1/auth/login
```

### Steps to Test Login

After following the step of the installation process and starting the server

1. Navigate to the login page
```bash
http://localhost:5000/login
```

2. Use any of the seeded users from the database.
   - Enter email and password

3. You will automatically be redirected to the Home/Index Page. Happy browsing!

### Steps to Test Adding a Review

The Add Review feature is only available to authenticated users.
It communicates with the backend endpoint:
```bash
POST /api/v1/reviews
```

User MUST follow the step above and be **logged in** to ensure the JWT cookie is set.

4. Navigate to any place details page, for example:
```bash
http://127.0.0.1:5000/place_details?place_id=a35837b8-25a2-49be-855d-84c1d0e8fe7a
```

5. Check for the “Add Review” button.
**Expected:**

- If logged in → The Add Review button appears below the place information.
- If not logged in → The button is hidden and you cannot access /add_review.

6. Click “Add Review”
This takes you to the form page
Submit a review:

- Enter a rating (e.g., 5)
- Enter a comment
- Click “Submit”

6. Expected Result
**A sucessful result:**
- An alert to notify "Review submitted successfully!"
- Once the user clicks "OK", they would be redirected to the place details page
- The new review appears under the Reviews section


## Technologies Used
### Frontend

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- Cookies for JWT storage
- Flask CORS

### Backend (existing from Part 3)

- Flask
- SQLAlchemy
- JWT Authentication
- Flask Bcrypt
- Flask Restx

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

- Define API namespaces for entities such as Users, Places, Amenities, Reviews.
- Handle request validation, serialization, and response formatting
- Manage authentication and authorization via JWTs
- Delegate business operations to the Facade Layer

Example:
When a client sends a request to /api/v1/users, the Presentation Layer:

- Validates the input using a Flask-RESTX model
- Calls the corresponding method in the Facade
- Returns a JSON response

It does not contain business logic; instead, it calls Facade methods to perform operations.
**Example usage:**

```
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserCreate(Resource):
   @api.expect(user_create_model, validate=True)
   @api.response(201, 'Admin successfully created')
   @api.response(400, 'Email already registered')
   @api.response(400, 'Invalid input data')
   @api.response(400, 'Invalid phone number')
   @api.response(400, 'Invalid password')
   @jwt_required()
   def post(self):
      # current_user = get_jwt()
      claims = get_jwt()
      if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

      user_data = api.payload
      email = user_data.get('email')

      # Check if email is already in use
      if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

      # Logic to create a new user
      try:
            # user_data = api.payload
            new_user = facade.create_user(user_data)
            return {
               'id': new_user.id,
               'message': "User registered sucessfully"
               }, 201
      except (TypeError,ValueError) as e:
            return {"error": str(e)}, 400
```

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

| Service            | Responsibility                                                        |
| ------------------ | --------------------------------------------------------------------- |
| UserService        | Manages user creation, authentication, updates, and admin privileges. |
| PlaceService       | Handle creation and management of property listings.                  |
| AmenityService     | Manage amenities associated with places.                              |
| ReviewService      | Process user reviews and ratings for places.                          |

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

  | Model   | Description                               | Key Attributes                                                                     |
  | ------- | ----------------------------------------- | ---------------------------------------------------------------------------------- |
  | Base    | Foundation for all entities.              | id, created_at, updated_at                                                         |
  | User    | Represents a HBnB platform user.          | id, first_name, last_name, email, password, phone number                           |
  | Place   | Property listed for rent.                 | id, owner_id, title, description, price, address, latitude, longitude, amenity_ids |
  | Amenity | Feature or facility available at a place. | id, name, description                                                              |
  | Review  | User feedback for a place.                | id, user_id, place_id, rating, comment, upload_image                               |

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

### Persistence Layer

The Persistence Layer handles all interactions with the database, abstracting SQLAlchemy queries from the rest of the application.
It consists of a generic repository for standard CRUD operations, and entity-specific repositories for additional domain-specific behaviors.

**Repository**
The SQLAlchemyRepository class provides a reusable base for all entities:

- Add objects to the database
- Retrieve single objects or all objects
- Update objects with new data
- Delete objects
- Query by attribute

**Entity-Specific Repositories**
Entity repositories inherit from SQLAlchemyRepository and add custom methods specific to that entity.

Example of User Repository:

```
   from app.models.user import User
   from app.persistence.repository import SQLAlchemyRepository

   class UserRepository(SQLAlchemyRepository):
      def __init__(self):
         super().__init__(User)

      def get_user_by_email(self, email):
         """Retrieve a user by their email address."""
         return self.model.query.filter_by(email=email).first()

```

## 🌐 API Endpoints

### 👥 Users

      1. GET /api/v1/users/  - Get all existing users
      2. GET /api/v1/users/{user_id}  - Get user details

### 🔰 Admin

      1. POST /api/v1/users/  - Admin can register new users
      2. PUT /api/v1/users/{user_id}  - Admin can update user information
      3. POST /api/v1/amenities/ - Admin can create amenities
      4. PUT /api/v1/amenities/{amenity_id} - Admin can update amenity

### 🛠️ Login

      1. POST /api/v1/auth/login - Any user can login with email and password
      2. GET /api/v1/auth/protected - A protected endpoint that requires JWT token

### 🏠 Places

      1. POST /api/v1/places/  - Create a new place
      2. GET /api/v1/places/   - Get all places
      3. GET /api/v1/places/{place_id} - Get place details
      4. PUT /api/v1/places/{place_id}  - Update place information
      5. DELETE /api/v1/places/{place_id} - Delete a place

### 📌 Amenities

      1. GET /api/v1/amenities/ - Get all amenities
      2. GET /api/v1/amenities/{amenity_id} - Get amenity details
      3. DELETE /api/v1/amenities/{amenity_id} - Admin can delete any amenity

### 📝 Reviews

      1. POST /api/v1/reviews/ - Create review
      2. GET /api/v1/reviews/ - Get all reviews
      3. GET /api/v1/reviews/{review_id} - Get review details
      4. PUT /api/v1/reviews/{review_id} - Update review
      5. DELETE /api/v1/reviews/{review_id} - Delete review


## 🌐 Admin Endpoints Example 🌐

### 1. Register a New User

**Endpoint** -- _POST /api/v1/users/_

**Request Body**

```json
{
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@example.com",
  "password": "password123"
}
```

**Response**

```json
{
  "id": "as235bjkfas882",
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@example.com",
}
```

### 2. Get User Details

**Endpoint** -- _GET /api/v1/users/{user_id}_

**Example Request**

```
GET /api/v1/users/as235bjkfas882
```

**Response**

```json
{
  "id": "as235bjkfas882",
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@example.com",
}
```

### 3. Update User Information

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
  "id": "as235bjkfas882",
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice@example.com",
}
```

## Entity-Relationship (ER) Database diagrams


The diagram below illustrates the database schema for the HBnB project, showing the main entities and their relationships. It defines how data is structured and interconnected across the application.

- User – Represents individuals using the platform. Each user can create multiple places and write multiple reviews.

- Place – Stores property information such as title, description, location, and price. Each place is owned by a user and can have many reviews and be linked to multiple amenities.

- Amenity – Represents features or services available at a place (e.g., Wi-Fi, pool). A place can have many amenities, and each amenity can belong to multiple places, forming a many-to-many relationship through the Place_Amenity table.

- Review – Contains user feedback for a place, linked to both the user who wrote it and the place being reviewed.

- Place_Amenity – A junction table that manages the many-to-many relationship between places and amenities.


This ERD ensures that the data model aligns with the project’s ORM (SQLAlchemy) implementation and supports clear relationships between users, places, amenities, and reviews.

![ER Diagram](ER_Diagram.png)

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.

