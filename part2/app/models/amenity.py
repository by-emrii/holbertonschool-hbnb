from app.models.base_model import BaseModel
# import re

class Amenity(BaseModel):
    def __init__(self, place_id, name, description=None):
        super().__init__()
        self.place_id = place_id
        self.name = name
        self.description = description

    """Getters and Setters"""
    """Amenity name"""
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Amenity name must be a string")
        
        value = value.strip()
        if len(value) > 0 and len(value)<= 50:
            self._name = value
        else:
            raise ValueError("Invalid amenity name length")

    """Amenity description"""
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value is None:
            self._description = None
            return
        
        if not isinstance(value, str):
            raise TypeError("Amenity description must be a string")
        
        value = value.strip()
        if len(value) > 0 and len(value)<= 100:
            self._description = value
        else:
            raise ValueError("Amenity description must be no more than 100 characters")
