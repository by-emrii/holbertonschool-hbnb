# Holberton School - HBnB Project

HBnB is a simplified Airbnb clone that allows users to manage accounts, list places, and handle reservations. The project demonstrates object-oriented design, software architecture, and persistence mechanisms.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
  - [Presentation Layer](#presentation-layer)
  - [Business Logic](#business-logic-layer)
  - [Persistence Layer](#persistence-layer)
- [Task 0: Presentation Layer](#task-0-presentation-layer)
- [Task 1: Business Logic](#task-1-business-logic)
- [Task 2: Sequence Diagrams](#task-2-sequence-diagrams)
- [Authors](#authors)

## Project Overview

HBnB allows users to create accounts, list properties, and make reservations. The project is divided into clear layers to separate concerns, making it modular and maintainable.

## Architecture

### Presentation Layer

- Handles user input and output
- Interacts with the business logic layer
- Exposes API endpoints or CLI commands
- Validates user requests

### Business Logic Layer

- Implements core functionalities such as user management, place listing, and reservations
- Enforces application rules and workflows
- Coordinates between presentation and persistence layers
- Handles data transformations

### Persistence Layer

- Stores and retrieves data from a database or file system
- Manages object serialization and deserialization
- Provides abstraction to isolate business logic from storage details
- Ensures data consistency and integrity

## Task 0: Package Diagram

![High Level Package Diagram](high_level_package_diagram.png)
<br>
**Key Components:**

### Presentation Layer

Handles user interactions, translating actions into system operations and displaying results.

- **UI:** Web interface for browsing, searching, and managing accounts.
- **API Endpoints:** Define routes for accessing features.
- **Controllers:** Validate inputs, call the Facade, and return responses.

### Business Layer

Core logic connecting Presentation and Persistence layers.

- **Facade Interface:** Entry point coordinating requests and delegating to services.
- **Service Models:** Contain reusable business rules (e.g., `UserService`, `PlaceService`, `ReviewService`, `BookingService`).
- **Domain Classes:** Core entities like `User`, `Place`, `Review`, `Amenity`, and `Reservation`.

### Persistence Layer

Manages data storage and retrieval.

- **Repository:** Handles CRUD operations (Create, Read, Update, Delete) and encapsulates database logic.
- **Database (MySQL):** Stores all application data.

## Task 1: Business Logic

![Business Logic Diagram](business_class_diagram.png)
<br>
**Entities:**

#### `User`

- Auth info, profile, and image
- Fields: `id`, `email`, `encrypted_password`, `phone_number`, `image_url`, etc.

#### `Place`

- Property listing info
- Fields: `id`, `user_id`, `title`, `description`, `price`, `location`, etc.

#### `Reservation`

- Tracks booking info
- Fields: `id`, `user_id`, `place_id`, `start_date`, `end_date`, `status`, etc.

#### `Amenity`

- Features or services offered at a place
- Fields: `id`, `name`, `description`, etc.

#### `Review`

- Feedback for a place
- Fields: `id`, `user_id`, `place_id`, `rating`, `comment`, `created_at`, etc.

## Task 2: Sequence Diagrams

diagram here

## Authors

- Crystal Chiam
- Grǎce Kayembe
- Emily Chew
