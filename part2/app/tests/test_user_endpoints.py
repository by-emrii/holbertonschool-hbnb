import unittest, uuid
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ---------- Helper Method ---------- #
    def create_sample_user(self):
       """ Helper to create a user for tests """

       unique = uuid.uuid4().hex[:6]
       self.sample_email = f"jane.doe.{unique}@example.com"

       # create a variable to catch response object returned by Flask
       response = self.client.post('/api/v1/users/', json={
           "first_name": "Jane",
           "last_name": "Doe",
           "email": self.sample_email,
           "phone_number": "+6123456789",
           "encrypted_password": "12345678"
       })
       
       # Convert JSON response to dict
       response_data = response.get_json()

       # Check fields in JSON response
       self.assertEqual(response_data.get("first_name"), "Jane")
       self.assertEqual(response_data.get("last_name"), "Doe")
       self.assertEqual(response_data.get("email"), self.sample_email)
       self.assertEqual(response_data.get("phone_number"), "+6123456789")

       # Check status code
       self.assertEqual(response.status_code, 201)
       return response
    
    # ---------- Tests ---------- #
    def test_create_user(self):
       """ Test creation of user profile """
       self.create_sample_user()

    def test_create_user_first_name_too_short(self):
        """Test creating a user with first name shorter than 2 characters"""
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "D",
            "last_name": "Johnson",
            "email": self.sample_email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_first_name_not_string(self):
        """Test creating a user where first name is not a string"""
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": 12345,
            "last_name": "Johnson",
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
    
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_last_name_too_short(self):
        """ Test creating a user with last name shorter than 2 characters """
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "L",
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_last_name_not_string(self):
        """ Test creating a user where last name is not a string """
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": 98765,
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
        
        self.assertEqual(response.status_code, 400)

    def test_create_user_email_in_use(self):
        """ Test creating a user with an email that already exists """
        # Create the first user
        self.create_sample_user()
        
        # Attempt to create another user with the same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": self.sample_email,
            "phone_number": "+6123456788",
            "encrypted_password": "abcdefgh"
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_email_format(self):
        """ Test creating a user with an invalid email format """
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}example.com"  # missing @
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_phone(self):
        """ Test creating a user with invalid phone number format """
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": email,
            "phone_number": "123ABC456",  # invalid format
            "encrypted_password": "abcdefgh"
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_short_password(self):
        """ Test creating a user with a password that is too short """
        unique = uuid.uuid4().hex[:6]
        email = f"user.{unique}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Charlie",
            "last_name": "Davis",
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "123"  # too short
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_byID(self):
        """ Test retrieving user by ID """
        # Create a user
        create_response = self.create_sample_user()

        # Extract user ID from response JSON
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        # Get user by ID
        get_response = self.client.get(f"/api/v1/users/{user_id}")
        response_data = get_response.get_json()

        self.assertEqual(response_data.get("first_name"), "Jane")
        self.assertEqual(response_data.get("last_name"), "Doe")
        self.assertEqual(response_data.get("email"), self.sample_email)
        self.assertEqual(response_data.get("phone_number"), "+6123456789")
        self.assertEqual(get_response.status_code, 200)
    
    def test_get_user_invalidID(self):
        """ Test get user by invalid ID """
        response = self.client.get(f'/api/v1/users/invalidID')
        self.assertEqual(response.status_code, 404)
    
    def test_update_user_details(self):
        """ Test update user details """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "phone_number": '+61123456788'
        })

        response_data = put_response.get_json()

        self.assertEqual(response_data.get("first_name"), "John")
        self.assertEqual(response_data.get("last_name"), "Smith")
        self.assertEqual(put_response.status_code, 200)
    
    def test_update_user_invalidID(self):
        """ Test updating a user with invalid ID """
        put_response = self.client.put(f'/api/v1/users/invalidID', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "phone_number": '+61123456788'
        })
        self.assertEqual(put_response.status_code, 404)
    
    def test_update_user_invalidInput(self): # (DOES NOT WORK)
        """ Test updating a user with invalid input """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "phone_number": '+61123456788'
        })

        self.assertEqual(put_response.status_code, 400)
