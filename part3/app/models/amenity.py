from app.models.base_model import BaseModel
from app.models.place import place_amenity
from sqlalchemy.orm import relationship, validates
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    places = relationship(
        'Place',
        secondary=place_amenity,
        back_populates='amenities',
        lazy=True
    )

    @validates("name")
    def validate_name(self, key, value):
        # 'name' valdiation and save
        if not isinstance(value, str):
            raise TypeError("Amenity name must be a string")
        
        value = value.strip()
        if len(value) <= 0:
            raise ValueError("Amenity name must not be empty")
        elif len(value) > 255:
            raise ValueError("Amenity name cannot exceed 255 characters")
        
        return value
        
    @validates("description")
    def validate_description(self, key, value):
    # 'description' validation and save
        if value is None:
            return None
        
        if not isinstance(value, str):
            raise TypeError("Amenity description must be a string")
        
        value = value.strip()
        if len(value) > 255:
            raise ValueError("Amenity description cannot exceed 255 characters")
        
        return value
