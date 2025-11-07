from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship, validates

# association table for Place <-> Amenity (many-to-many)
# one Place can have many Amenitys + one Amenity can belong to many Places
# so we need an association table

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True),
)


""" Class Place represents to Place model in BL"""
class Place(BaseModel):
    __tablename__ = 'places'

    # Core attributes as required by task_08, except amenity_ids and review_ids
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    address = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String, nullable=True)

    # Foreign Key for User-Place relationship (One-to-Many)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # =====================
    # RELATIONASHIPS
    # =====================

    # many Places -> one User
    # no need define owner in place, as place is defined in user by backref.
    # owner = relationship('User', back_populates='places')

    # one Place -> many Reviews
    reviews = relationship('Review', backref='place', lazy=True)

    # many-to-many Place <-> Amenity
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        lazy='subquery'
    )
    
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
    # HELPER METHODS
    # =====================

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
