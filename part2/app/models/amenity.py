from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=None):
        super().__init__()
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
        elif len(value) <= 0:
            raise ValueError("Amenity name must not be empty")
        elif len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")

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
            raise ValueError("Amenity description cannot exceed 100 characters")
