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
- If not logged in → The button is hidden and you cannot access /add_review.

**6. Click “Add Review”**
This takes you to the form page
Submit a review:

- Enter a rating (e.g., 5)
- Enter a comment
- Click “Submit”

**6. Expected Result**

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

