import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ---------- Create Sample Amenity ---------- #
    def create_sample_amenity(self):
        """ Create amenity """
        """ Test creation of amenity """
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Wi-Fi',
            'description': '5G Internet'
        })
        
        response_data = response.get_json()
        # Check fields in JSON response
        self.assertEqual(response_data.get("name"), "Wi-Fi")
        self.assertEqual(response_data.get("description"), "5G Internet")
        self.assertEqual(response.status_code, 201)
        return response

    # ---------- Tests ---------- #
    def test_create_amenity(self):
       self.create_sample_amenity()
    
    def test_create_invalid_amenity(self):
       """ Test creation of amenity with invalid data """
       response = self.client.post('/api/v1/amenities/', json={
           'name': '',
           'description': ''
       })
       
       self.assertEqual(response.status_code, 400)
    
    def test_get_amenity_byID(self):
        """ Test get amenity by ID """
        create_response = self.create_sample_amenity()
        amenity_data = create_response.get_json()
        amenity_id = amenity_data.get("id")
        
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_invalidID(self):
        """ Test get amenity by invalid ID """
        response = self.client.get(f'/api/v1/amenities/invalidID')
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_amenities(self):
        """ Test get all amenities """
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
    
    # def test_get_no_amenities(self): -> to implement when we create 'Delete' in part 3
    #     """ Test get all amenities when no amenities exist """
    #     response = self.client.get('api/v1/amenities/')
    #     self.assertEqual(response.status_code, 404)
    
    def test_update_amenity(self):
        """ Test updating an amenity by ID """ 
        create_response = self.create_sample_amenity()
        amenity_data = create_response.get_json()
        amenity_id = amenity_data.get("id")

        put_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Dial-Up Internet",
            "description": "It's really slow"
        })

        response_data = put_response.get_json()

        self.assertEqual(response_data.get("name"), "Dial-Up Internet")
        self.assertEqual(response_data.get("description"), "It's really slow")
        self.assertEqual(put_response.status_code, 200)

    def test_update_amenity_invalidID(self):
        """ Test updating an amenity with invalid ID """
        put_response = self.client.put(f'/api/v1/amenities/invalidID', json={
            "name": "Dial-Up Internet",
            "description": "It's really slow"
        })
        self.assertEqual(put_response.status_code, 404)

    def test_update_amenity_invalidInput(self):
        """ Test updating an amenity with invalid input """
        create_response = self.create_sample_amenity()
        amenity_data = create_response.get_json()
        amenity_id = amenity_data.get("id")

        put_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "",
            "description": ""
        })

        self.assertEqual(put_response.status_code, 400)
