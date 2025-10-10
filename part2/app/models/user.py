from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, encrypted_password, phone_number, profile_img, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__encrypted_password = encrypted_password
        self.phone_number = phone_number
        self.profile_img = profile_img
        self.is_admin = is_admin

    """ Getters and Setters """
    """ First Name """
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        value = value.strip()
        if len(value) < 2:
            raise ValueError("First name must be at least 2 characters")
        if len(value) >= 50:
            raise ValueError("First name cannot be more than 50 characters")
        self._first_name = value
    
    """ Last name """