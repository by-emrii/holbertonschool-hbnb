import unittest
from uuid import uuid4
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create an User as Owner
        unique = uuid4().hex[:6]
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Sylvia",
            "last_name": "Xie",
            "email": f"sylvia_{unique}@test.com",   # make sure the email is unique
            "phone_number": "+61412345678",
            "encrypted_password": "password123"
        })
        # throw err msg if failed
        if user_response.status_code != 201:
            print("Create user failed:", user_response.status_code, user_response.get_json())
        self.assertEqual(user_response.status_code, 201)
        self.owner_id = user_response.get_json().get("id")

    # ---------- Helper ---------- #
    def create_sample_place(self):
        """Create a sample place for testing"""
        response = self.client.post('/api/v1/places/', json={
            "user_id":self.owner_id,
            "title":"Cozy Flat",
            "description":"Nice 2-bedroom flat near city center",
            "price":240.0,
            "address":"888 Main St, Melbourne",
            "latitude":-24.7241,
            "longitude":124.6281,
            "image_url":"https://example.com/image.jpg",
            "amenity_ids":["1", "2", "2", "3"]  #  test for removing duplicate ids
        })
        self.assertEqual(response.status_code, 201)
        return response

    # ---------- Tests ---------- #
    def test_create_place(self):
        response = self.create_sample_place()
        data = response.get_json()
        self.assertEqual(data.get("title"), "Cozy Flat")
        self.assertEqual(data.get("price"), 240.0)
        self.assertEqual(data.get("amenity_ids"), ["1", "2", "3"])

    def test_create_place_invalid_user(self):
        """Test for non-exist user_id and return 400"""
        response = self.client.post('/api/v1/places/', json={
            "user_id": "invalid-user",
            "title": "Invalid Place",
            "price": 240,
            "latitude": -24.7241,
            "longitude": 124.6281
        })
        self.assertEqual(response.status_code, 400)


    def test_get_place_by_id(self):
        create_response = self.create_sample_place()
        place_id = create_response.get_json().get("id")
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("id"), place_id)

    def test_get_place_invalid_id(self):
        response = self.client.get('/api/v1/places/invalidID')
        self.assertEqual(response.status_code, 404)

    def test_get_all_places(self):
        """ Test get all places """
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        create_response = self.create_sample_place()
        place_id = create_response.get_json().get("id")

        put_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Flat",
            "price": 200
        })
        self.assertEqual(put_response.status_code, 200)
        updated = put_response.get_json()
        self.assertEqual(updated.get("title"), "Updated Flat")

    def test_update_place_invalid_id(self):
        response = self.client.put('/api/v1/places/invalidID', json={
            "title": "Fail Update"
        })
        self.assertEqual(response.status_code, 404)

    def test_get_place_includes_amenities_details(self):
        # create amenities
        a1 = self.client.post('/api/v1/amenities/', json={"name": "Wifi", "description": "Fast internet"})
        a2 = self.client.post('/api/v1/amenities/', json={"name": "Pool", "description": "Outdoor"})
        a3 = self.client.post('/api/v1/amenities/', json={"name": "Parking", "description": "Free"})
        self.assertEqual(a1.status_code, 201)
        self.assertEqual(a2.status_code, 201)
        self.assertEqual(a3.status_code, 201)
        amenity_ids = [a1.get_json()["id"], a2.get_json()["id"], a3.get_json()["id"]]

        # create place referencing amenities
        create_resp = self.client.post('/api/v1/places/', json={
            "user_id": self.owner_id,
            "title": "Amenity Rich Flat",
            "description": "Has many amenities",
            "price": 300.0,
            "address": "1 Test St",
            "latitude": -24.0,
            "longitude": 124.0,
            "amenity_ids": amenity_ids,
        })
        self.assertEqual(create_resp.status_code, 201)
        place_id = create_resp.get_json()["id"]

        # get by id should include amenities array with details
        get_resp = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_resp.status_code, 200)
        body = get_resp.get_json()
        self.assertIn("amenity_ids", body)
        self.assertIn("amenities", body)
        self.assertEqual(sorted(body["amenity_ids"]), sorted(amenity_ids))
        self.assertEqual(len(body["amenities"]), 3)
        names = {a["name"] for a in body["amenities"]}
        self.assertTrue({"Wifi", "Pool", "Parking"}.issubset(names))

        # list should also include amenities details
        list_resp = self.client.get('/api/v1/places/')
        self.assertEqual(list_resp.status_code, 200)
        items = list_resp.get_json()
        self.assertIsInstance(items, list)
        # find our place
        found = next((p for p in items if p.get("id") == place_id), None)
        self.assertIsNotNone(found)
        self.assertIn("amenity_ids", found)
        self.assertIn("amenities", found)
        self.assertEqual(sorted(found["amenity_ids"]), sorted(amenity_ids))
        self.assertEqual(len(found["amenities"]), 3)

