import unittest
from app import create_app
# from app.services.facade import user_repo

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        # run a fresh Flask app instance for testing
        self.app = create_app()
        # create a testing client to simulate HTTP responses
        #self.client can send GET, POST, PUT etc
        # self.client can return response objects (with .status_code, .json)
        self.client = self.app.test_client()
        print("Setting up")
    
    # def tearDown(self):
    #     """Reset repository after each test"""
    #     user_repo._storage.clear()
    #     print("Repo cleared, remaining:", len(user_repo._storage))
    
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
       # print(response.get_data(as_text=True))
       
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
       print("Running test one")
    
    # def test_create_user_invalid_data(self):
    #     """ Test creating user with invalid data"""
    #     response = self.client.post('/api/v1/users/', json={
    #         "first_name": "",
    #         "last_name": "",
    #         "email": "invalid-email",
    #         "phone_number": "0123456789",
    #         "encrypted_password": "0000"
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     print("Running test two")

    def test_get_user_byID(self):
        """ Test retrieving user by ID """
        # Create a user
        create_response = self.create_sample_user()

        # Extract user ID from response JSON
        user_data = create_response.get_json()
        user_id = user_data.get("id")

        print(create_response.get_data(as_text=True))
        print(user_id)

        # Get user by ID
        get_response = self.client.get(f"/api/v1/users/{user_id}")
        response_data = get_response.get_json()

        self.assertEqual(response_data.get("first_name"), "Jane")
        self.assertEqual(response_data.get("last_name"), "Doe")
        self.assertEqual(response_data.get("email"), "jane.doe@example.com")
        self.assertEqual(response_data.get("phone_number"), "+6123456789")
        self.assertEqual(get_response.status_code, 200)
        print("Running test two")
    
    # def test_get_user_invalidID(self):
    #     """ Test get user by invalid ID """
    #     response = self.client.get(f'/api/v1/users/invalidID')
    #     self.assertEqual(response.status_code, 404)
    
    # def test_update_user_details(self):
    #     """ Test update user details """
    #     create_response = self.create_sample_user()
    #     user_data = create_response.get_json()
    #     user_id = user_data.get("id")

    #     put_response = self.client.put(f'/api/v1/users/{user_id}', json={
    #         "first_name": "John",
    #         "last_name": "Smith",
    #         "email": "john.smith@example.com",
    #         "phone_number": '+61123456788'
    #     })

    #     response_data = put_response.get_json()

    #     self.assertEqual(response_data.get("first_name"), "John")
    #     self.assertEqual(response_data.get("last_name"), "Smith")
    #     self.assertEqual(put_response.status_code, 200)
    
    # def test_update_user_invalidID(self):
    #     """ Test updating a user with invalid ID """
    #     put_response = self.client.put(f'/api/v1/users/invalidID', json={
    #         "first_name": "John",
    #         "last_name": "Smith",
    #         "email": "john.smith@example.com",
    #         "phone_number": '+61123456788'
    #     })
    #     self.assertEqual(put_response.status_code, 404)
    
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
