from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re

""" Class Place represents to Place model in BL"""


class Place(BaseModel):
    __tablename__ = 'places'

    # Core attributes as required by task_08, except amenity_ids and review_ids
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Additional attributes from business logic (not mapped as relationships yet)
    owner_id = db.Column(db.String(36), nullable=False)  # Will be foreign key in later task
    address = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String, nullable=True)

    # amenity_ids and review_ids will be handled via relationships in later tasks
    # For now, we won't persist them as they represent relationships

    # =====================
    # VALIDATORS
    # =====================
    
    @validates('owner_id')
    def validate_owner_id(self, key, value):
        """Validate owner_id"""
        if isinstance(value, int):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError("Owner ID must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Owner ID cannot be empty")
        return value

    @validates('title')
    def validate_title(self, key, value):
        """Validate place title"""
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return value

    @validates('description')
    def validate_description(self, key, value):
        """Validate description"""
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        value = value.strip()
        if len(value) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        """Validate price"""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        value = float(value)
        if value < 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        """Validate latitude"""
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        value = float(value)
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        """Validate longitude"""
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        value = float(value)
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return value

    @validates('address')
    def validate_address(self, key, value):
        """Validate address"""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Address must be a string")
        value = value.strip()
        if len(value) < 5 or len(value) > 200:
            raise ValueError("Address must be between 5 and 200 characters")
        return value

    @validates('image_url')
    def validate_image_url(self, key, value):
        """Validate image URL"""
        if value is None or str(value).strip() == "":
            return None
        if not isinstance(value, str):
            raise TypeError("image_url must be a string")
        value = value.strip()
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("image_url must start with http(s)://")
        return value

    # =====================
    # UTILITY METHODS
    # =====================
    # These methods handle amenity_ids and review_ids temporarily
    # They will be replaced with proper relationships in later tasks
    
    @property
    def amenity_ids(self):
        """Temporary property for amenity_ids (will be replaced with relationship)"""
        return getattr(self, '_amenity_ids', [])
    
    @amenity_ids.setter
    def amenity_ids(self, value):
        """Temporary setter for amenity_ids"""
        if not isinstance(value, list):
            raise TypeError("Amenity IDs must be a list")
        cleaned = list(dict.fromkeys(str(v).strip() for v in value if v))
        self._amenity_ids = cleaned

    @property
    def review_ids(self):
        """Temporary property for review_ids (will be replaced with relationship)"""
        return getattr(self, '_review_ids', [])

    @review_ids.setter
    def review_ids(self, value):
        """Temporary setter for review_ids"""
        if not isinstance(value, list):
            raise TypeError("Review IDs must be a list")
        cleaned = list(dict.fromkeys(str(v).strip() for v in value if v))
        self._review_ids = cleaned

    def add_amenity(self, amenity_id):
        """Add an amenity to the place (temporary method)"""
        if amenity_id is None:
            return
        aid = str(amenity_id).strip()
        if not aid:
            return
        current = list(getattr(self, "amenity_ids", []) or [])
        current.append(aid)
        self.amenity_ids = current

    def add_review(self, review_id):
        """Add a review to the place (temporary method)"""
        if review_id is None:
            return
        rid = str(review_id).strip()
        if not rid:
            return
        current = list(getattr(self, "review_ids", []) or [])
        current.append(rid)
        self.review_ids = current
