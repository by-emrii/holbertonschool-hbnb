import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        # run a fresh Flask app instance for testing
        self.app = create_app()
        # create a testing client to simulate HTTP responses
        #self.client can send GET, POST, PUT etc
        # self.client can return response objects (with .status_code, .json)
        self.client = self.app.test_client()
    
    # ---------- Helper Method ---------- #
    def create_sample_user(self):
       """ Helper to create a user for tests """
       # create a variable to catch response object returned by Flask
       response = self.client.post('/api/v1/users/', json={
           "first_name": "Jane",
           "last_name": "Doe",
           "email": "jane.doe@example.com",
           "phone_number": "+6123456789",
           "encrypted_password": "12345678"
       })
       # print response for debugging
       print(response.get_data(as_text=True))
       
       # Convert JSON response to dict
       response_data = response.get_json()

       # Check fields in JSON response
       self.assertEqual(response_data.get("first_name"), "Jane")
       self.assertEqual(response_data.get("last_name"), "Doe")
       self.assertEqual(response_data.get("email"), "jane.doe@example.com")
       self.assertEqual(response_data.get("phone_number"), "+6123456789")

       # Check status code
       self.assertEqual(response.status_code, 201)
       return response
    
    # ---------- Tests ---------- #
    def test_create_user(self):
       """ Test creation of user profile """
       self.create_sample_user()
    
    def test_create_user_invalid_data(self):
        """ Test creating user with invalid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "phone_number": "0123456789",
            "encrypted_password": "0000"
        })
        self.assertEqual(response.status_code, 400)

    # def test_get_user_byID(self):
    #     """ Test retrieving user by ID """
    #     # Create a user
    #     create_response = self.create_sample_user()

    #     # Extract user ID from response JSON
    #     user_data = create_response.get_json()
    #     user_id = user_data.get("id")

    #     # Get user by ID
    #     get_response = self.client.get(f"/api/v1/users/{user_id}")
    #     self.assertEqual(get_response.status_code, 200)
