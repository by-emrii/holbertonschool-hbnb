from app import db
from app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt
import re
from sqlalchemy.orm import validates, relationship

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String, nullable=True)
    profile_img = db.Column(db.String, nullable=True)

    # =====================
    # RELATIONSHIPS
    # =====================
    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='author', lazy=True)

    # =====================
    # VALIDATORS
    # =====================
    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        """ First and last name validations """
        if not isinstance(value, str):
            raise TypeError(f"{key.replace('_',' ').title()} must be a string")
        value = value.strip()
        if len(value) > 50:
            raise ValueError(f"{key.replace('_', ' ').title()} cannot exceed 50 characters")
        return value
    

    @validates('email')
    def validate_email(self, key, value):
        """ Email validation with email format using regex """
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        value = value.strip().lower()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address format")
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Phone number must be a string")
        value = value.strip()
        phone_regex = r'^\+?[1-9]\d{1,14}$'
        if not re.match(phone_regex, value):
            raise ValueError("Invalid phone number format, for example: +61(CountryCode) XXXX XXXX")
        return value      

    # =====================
    # PASSWORD HASHING
    # =====================
    def hash_password(self, password): 
        """ Hashes the password before storing it """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """ Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)