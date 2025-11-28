# 🏠 Holberton School HBnB Project Part 4 - Simple Web Client

This project implements the frontend interface for the HBNB accommodation platform, completing Part 4 of the Holberton School full-stack series.

It connects a custom Flask API (from Part 3) with a fully functional web client built using **HTML5, CSS3, and JavaScript ES6**.

The result is a lightweight, interactive application where users can:

- Authenticate using JWT
- Browse and filter places
- View detailed place information
- Submit reviews (authenticated users only)

The frontend is designed for simplicity, responsiveness, and clean API communication.

# 📚 Table of Contents

1. [Project Overview](#-holberton-school-hbnb-project-part-4---simple-web-client)  
2. [Project Structure](#project-structure)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Features Delivered](#features-delivered)  
   - [1. Authentication (JWT Login)](#-1-authentication-jwt-login)  
   - [2. Places List (Home Page)](#-2-places-list-home-page)  
   - [3. Place Details Page](#-3-place-details-page)  
   - [4. Add Review Page](#-4-add-review-page)  
6. [JavaScript Implementation Overview](#️-javascript-implementation-overview)  
7. [UI & Styling](#-ui--styling)  
8. [How to Test the Login and Add Review Functionality](#how-to-test-the-login-and-add-review-functionality)  
9. [Technologies Used](#technologies-used)  
10. [License](#-license)

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

## Features Delivered
### 🔐 1. Authentication (JWT Login)

- Users log in via `/api/v1/auth/login`
- On success, a JWT token is stored in cookies
- All protected pages verify authentication before rendering
- If no token → redirect to the Login page

Frontend implemented:

- Login form UI
- Error handling for invalid credentials
- Cookie storage
- UI state updates based on authentication

### 🏠 2. Places List (Home Page)
**Data:**

Fetched from:
```bash
GET /api/v1/places
```

**Features:**

- Display all places with:
   - Name
   - Image
   - Price
   - Average Rating
- Dropdown filter by price (client-side filtering)
- Clicking a place opens its details page

**UI:**

- Fully responsive layout
- Card-based display of places
- Clean separation of HTML + CSS + JS

### 📍 3. Place Details Page
**Data:**

Fetched from:
```bash
GET /api/v1/places/<id>
```

**Display:**

- Place name
- Price
- Description
- Image
- Average rating
- Amenities
- List of existing reviews

**Additional Features:**

- “Add Review” button shows only if a user is logged in

### 📝 4. Add Review Page
**Function:**

Allows authenticated users to create a review for a place.

**Implementation:**

```bash
POST /api/v1/places
```

**Features:**

- Form validation
- Redirect on success back to the place details
- Error messaging for invalid submissions


## 🛠️ JavaScript Implementation Overview
Each page has its own JS module:

  | File              | Purpose                                         |
  | ----------------- | ----------------------------------------------- |
  | login.js          | Handles user login, token storage, redirects    |
  | index.js          | Fetches places, renders list, handles filtering |
  | place_details.js  | Fetches place details + reviews                 |
  | add_review.js     | Submits new reviews                             |

- Shared Logic
- Cookie-based token checking
- Redirect helpers
- Standardized API calls via Fetch API
- DOM creation using template literals

## 🎨 UI & Styling

The UI was designed to follow clean, modern principles:

- Responsive layout
- Modular CSS per page
- Consistent colors and spacing
- Shared header and footer templates
- Simple, intuitive navigation


## How to Test the Login and Add Review Functionality

The login feature is implemented on the `/login` page.

This page communicates with the backend authentication endpoint:

```bash
POST /api/v1/auth/login
```

### Steps to Test Login

After following the step of the installation process and starting the server:

**1. Navigate to the login page**
```bash
http://localhost:5000/login
```

**2. Use any of the seeded users from the database**
   - Enter `email` and `password`

**3. You will automatically be redirected to the Home/Index Page. Happy browsing!**

### Steps to Test Adding a Review

The Add Review feature is only available to authenticated users.

It communicates with the backend endpoint:
```bash
POST /api/v1/reviews
```

> User MUST follow the step above and be **logged in** to ensure the JWT cookie is set.

**4. Navigate to any place details page, for example:**
```bash
http://127.0.0.1:5000/place_details?place_id=a35837b8-25a2-49be-855d-84c1d0e8fe7a
```

**5. Check for the “Add Review” button**

**Expected:**

- If logged in → The Add Review button appears below the place information.
- If not logged in → The button is hidden and you cannot access `/add_review`.

**6. Click “Add Review”**
This takes you to the form page
Submit a review:

- Enter a rating (e.g., 5)
- Enter a comment
- Click “Submit”

**7. Expected Result**
- If user has already reviewed:
Outcome: "You have already reviewed this place."
- If owner tries to review place: 
Outcome: "You cannot not review a place you own."
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


## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.




