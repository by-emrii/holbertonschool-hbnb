from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, phone_number, profile_img=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
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
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Last name must be at least 2 characters")
        if len(value) >= 50:
            raise ValueError("Last name cannot be more than 50 characters")
        self._last_name = value
    
    """ Email """
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        value = value.strip().lower()
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        self._email = value
    
    """Phone Number"""
    @property
    def phone_number(self):
        return self._phone_number
    
    @phone_number.setter
    def phone_number(self, value):
        phone_regex = r'^\+?[1-9]\d{1,14}$'
        if not isinstance(value, str):
            raise TypeError("Phone number must be a string")
        value = value.strip()
        if not re.match(phone_regex, value):
            raise ValueError("Invalid phone number format, for example: +61(CountryCode) XXXX XXXX")
        self._phone_number = value        

    """Password"""
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        value = value.strip()

        #password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8}$"
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.__password = value        
