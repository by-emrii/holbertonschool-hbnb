import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ---------- Tests ---------- #
    def test_create_amenity(self):
       """ Test creation of amenity """
       response = self.client.post('api/v1/amenities/', json={
           'name': 'Wi-Fi',
           'description': '5G Internet'
       })
       
       response_data = response.get_json()
       # Check fields in JSON response
       self.assertEqual(response_data.get("name"), "Wi-Fi")
       self.assertEqual(response_data.get("description"), "5G Internet")
       self.assertEqual(response.status_code, 201)
    
    def test_create_invalid_amenity(self):
       """ Test creation of amenity with invalid data """
       response = self.client.post('api/v1/amenities/', json={
           'name': '',
           'description': ''
       })
       
       self.assertEqual(response.status_code, 400)