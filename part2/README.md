# 🏠 Holberton School - HBnB Project Part 2
HBnB is a simplified clone of the Airbnb platform. It’s designed to teach the fundamentals of back-end development, RESTful API design, and modular architecture using Python and Flask.


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



