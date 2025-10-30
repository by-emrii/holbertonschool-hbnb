import unittest
from app import create_app
from app.models.review import Review

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        """ Initialize Flask app and test client """
        self.app = create_app()
        self.client = self.app.test_client()

<<<<<<< HEAD
    # Create a real user
=======
    # Create main user
>>>>>>> review/grace
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone_number": "+6112345678",
            "encrypted_password": "password123"
        })
        self.user_id = user_resp.get_json()["id"]

<<<<<<< HEAD
        # Create a real place
=======
        # Create another user for forbidden tests
        another_user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Another",
            "last_name": "User",
            "email": "anotheruser@example.com",
            "phone_number": "+6112345679",
            "encrypted_password": "password123"
        })
        self.another_user_id = another_user_resp.get_json()["id"]

        # Create a test place
>>>>>>> review/grace
        place_resp = self.client.post('/api/v1/places/', json={
            "user_id": self.user_id,
            "title": "Test Place",
            "description": "A place for testing",
            "price": 100,
            "address": "123 Test St",
            "latitude": 0.0,
            "longitude": 0.0,
            "image_url": "https://example.com/place.jpg"
        })
        self.place_id = place_resp.get_json()["id"]

<<<<<<< HEAD
    # Create Sample Review 
    def create_sample_review(self):
        """ Helper method to create a sample review """
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
=======
    # Helper method to create a sample review
    def create_sample_review(self, user_id=None):
        user_id = user_id or self.user_id
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": user_id,
>>>>>>> review/grace
            "place_id": self.place_id,
            "rating": 4,
            "text": "Nice stay!",
            "upload_image": ["https://example.com/image.jpg"]
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        return data

    # Create Tests
    def test_create_review_success(self):
        review = self.create_sample_review()
        self.assertEqual(review.get("rating"), 4)
        self.assertEqual(review.get("text"), "Nice stay!")

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 10,
            "text": "Invalid rating"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertIn("rating", data["error"].lower())

    def test_create_review_missing_fields(self):
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 4,
            "text": "Incomplete data"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    # Read Tests
    def test_get_review_by_id(self):
        review = self.create_sample_review()
        review_id = review.get("id")
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), review_id)
        self.assertEqual(data.get("user_id"), self.user_id)

    def test_get_review_invalid_id(self):
        response = self.client.get('/api/v1/reviews/invalidID')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    # Update Tests
    def test_update_review_success(self):
        review = self.create_sample_review()
        review_id = review.get("id")
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 5,
            "text": "Even better!",
<<<<<<< HEAD
            "current_user_id": "user123"
=======
            "current_user_id": self.user_id
>>>>>>> review/grace
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("rating"), 5)
        self.assertEqual(data.get("text"), "Even better!")

    def test_update_review_invalid_id(self):
        response = self.client.put('/api/v1/reviews/invalidID', json={
            "rating": 3,
            "text": "Invalid test",
<<<<<<< HEAD
            "current_user_id": "user123"
=======
            "current_user_id": self.user_id
>>>>>>> review/grace
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    def test_update_review_forbidden_user(self):
        review = self.create_sample_review()
        review_id = review.get("id")
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 2,
            "text": "Not allowed",
<<<<<<< HEAD
            "current_user_id": "another_user"
=======
            "current_user_id": self.another_user_id
>>>>>>> review/grace
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", data)

    #Delete Tests
    def test_delete_review_success(self):
        review = self.create_sample_review()
        review_id = review.get("id")
        response = self.client.delete(f'/api/v1/reviews/{review_id}', json={
            "current_user_id": self.user_id
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Review deleted successfully")

    def test_delete_review_forbidden_user(self):
        review = self.create_sample_review()
        review_id = review.get("id")
        response = self.client.delete(f'/api/v1/reviews/{review_id}', json={
            "current_user_id": self.another_user_id
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", data)

    def test_delete_review_invalid_id(self):
        response = self.client.delete('/api/v1/reviews/invalidID', json={
            "current_user_id": self.user_id
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    # List Tests
    def test_list_reviews_by_place(self):
        self.create_sample_review()
        response = self.client.get(f'/api/v1/reviews/place/{self.place_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("place_id"), self.place_id)

    def test_list_reviews_by_place_not_found(self):
        response = self.client.get('/api/v1/reviews/place/noPlace')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_list_reviews_by_user(self):
        self.create_sample_review()
        response = self.client.get(f'/api/v1/reviews/user/{self.user_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("user_id"), self.user_id)

    def test_list_reviews_by_user_not_found(self):
        response = self.client.get('/api/v1/reviews/user/noUser')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)