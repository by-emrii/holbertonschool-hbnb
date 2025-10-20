import unittest
from uuid import uuid4
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a user to submit reviews
        unique = uuid4().hex[:6]
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": f"reviewer_{unique}@test.com",
            "phone_number": "+61412345678",
            "encrypted_password": "password123"
        })
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json().get("id")

        # Create a user to own a place
        owner_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": f"owner_{unique}@test.com",
            "phone_number": "+61412345679",
            "encrypted_password": "password123"
        })
        self.assertEqual(owner_resp.status_code, 201)
        self.owner_id = owner_resp.get_json().get("id")

        # Create a test place
        place_resp = self.client.post('/api/v1/places/', json={
            "user_id": self.owner_id,
            "title": "Test Place",
            "description": "A nice test place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        })
        self.assertEqual(place_resp.status_code, 201)
        self.place_id = place_resp.get_json().get("id")

    def test_create_review(self):
        response = self.client.post(f'/api/v1/places/{self.place_id}/reviews/', json={
            "user_id": self.user_id,
            "rating": 5,
            "comment": "Amazing stay!"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["comment"], "Amazing stay!")

    def test_get_reviews_for_place(self):
        # create review first
        self.client.post(f'/api/v1/places/{self.place_id}/reviews/', json={
            "user_id": self.user_id,
            "rating": 4,
            "comment": "Good place"
        })
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
