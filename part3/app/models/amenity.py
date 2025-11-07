from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)

    @validates("name")
    def validate_name(self, key, value):
        # 'name' valdiation and save
        if not isinstance(value, str):
            raise TypeError("Amenity name must be a string")
        
        value = value.strip()
        if len(value) <= 0:
            raise ValueError("Amenity name must not be empty")
        elif len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        
        return value
        
    @validates("description")
    def validate_description(self, key, value):
    # 'description' validation and save
        if value is None:
            return None
        
        if not isinstance(value, str):
            raise TypeError("Amenity description must be a string")
        
        value = value.strip()
        if len(value) > 100:
            raise ValueError("Amenity description cannot exceed 100 characters")
        
        return value

    # """Getters and Setters"""
    # """Amenity name"""
    # @property
    # def name(self):
    #     return self._name
    
    # @name.setter
    # def name(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError("Amenity name must be a string")
        
    #     value = value.strip()
    #     if len(value) > 0 and len(value)<= 50:
    #         self._name = value
    #     elif len(value) <= 0:
    #         raise ValueError("Amenity name must not be empty")
    #     elif len(value) > 50:
    #         raise ValueError("Amenity name cannot exceed 50 characters")

    # """Amenity description"""
    # @property
    # def description(self):
    #     return self._description
    
    # @description.setter
    # def description(self, value):
    #     if value is None:
    #         self._description = None
    #         return
        
    #     if not isinstance(value, str):
    #         raise TypeError("Amenity description must be a string")
        
    #     value = value.strip()
    #     if len(value) > 0 and len(value)<= 100:
    #         self._description = value
    #     else:
    #         raise ValueError("Amenity description cannot exceed 100 characters")
