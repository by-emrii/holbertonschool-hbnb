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
            "email": email,
            "phone_number": "+6123456789",
            "encrypted_password": "password123"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("at least 2", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name must be a string", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name must be a string", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name must be at least 2 characters", data.get('error', '').lower())

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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("already used", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid email", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid phone", data.get('error', '').lower())
    
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
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("at least 8", data.get('error', '').lower())

    # Get all users
    def test_get_all_users(self):
        """ Test get all users """
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

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
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", data.get('error', '').lower())
    
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
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 404)
        self.assertIn("not found", data.get('error', '').lower())
    
    def test_update_user_first_name_too_short(self):
        """ Test updating a user with invalid first name """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "",
            "last_name": "Smith",
            "email": "jim.smith@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("at least 2", data.get('error', '').lower())

    def test_update_user_last_name_too_short(self):
        """ Test updating a user with invalid first name """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "",
            "email": "john.short@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("at least 2", data.get('error', '').lower())
    
    def test_update_user_first_name_not_string(self):
        """ Test updating a user where first name is not a string """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": 12345,
            "last_name": "String",
            "email": "john.string@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("name must be a string", data.get('error', '').lower())
    
    def test_update_user_last_name_not_string(self):
        """ Test updating a user where last name is not a string """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": 12345,
            "email": "john.strong@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("name must be a string", data.get('error', '').lower())

    def test_update_user_first_name_too_short(self):
        """ Test updating a user where first name is too short """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "J",
            "last_name": "Hope",
            "email": "j.hope@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("at least 2", data.get('error', '').lower())
    
    def test_update_user_last_name_too_short(self):
        """ Test updating a user where last name is too short """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Helly",
            "last_name": "R",
            "email": "Helly.R@example.com",
            "phone_number": '+61123456788'
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("at least 2", data.get('error', '').lower())
    
    def test_update_user_email_in_use(self):
        """ Test updating a user with an email that already exists """
        # Create two users
        first_user_response = self.create_sample_user()
        first_user = first_user_response.get_json()

        second_user_response = self.create_sample_user()
        second_user = second_user_response.get_json()
        second_user_id = second_user.get("id")

        # Attempt to update the second user with the first user's email
        put_response = self.client.put(f'/api/v1/users/{second_user_id}', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": first_user.get("email"),  # duplicate email
            "phone_number": "+6123456788"
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("already in use", data.get('error', '').lower())
    
    def test_update_user_invalid_email_format(self):
        """ Test updating a user with an invalid email format """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        invalid_email = "invalid.email.example.com"  # missing '@'
        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": invalid_email,
            "phone_number": "+6123456789"
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("invalid email", data.get('error', '').lower())
    
    def test_update_user_invalid_phone(self):
        """ Test updating a user with invalid phone number format """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": user_data.get("email"),
            "phone_number": "123ABC456"  # invalid format
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("invalid phone", data.get('error', '').lower())
    
    def test_update_user_short_password(self):
        """ Test updating a user with a password that is too short """
        create_response = self.create_sample_user()
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        put_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Charlie",
            "last_name": "Davis",
            "email": user_data.get("email"),
            "phone_number": "+6123456789",
            "encrypted_password": "123"  # too short
        })
        data = put_response.get_json()
        self.assertEqual(put_response.status_code, 400)
        self.assertIn("at least 8", data.get('error', '').lower())
