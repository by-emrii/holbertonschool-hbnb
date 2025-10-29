import unittest
from app import create_app
from app.models.review import Review

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        """ Initialize Flask app and test client """
        self.app = create_app()
        self.client = self.app.test_client()

    # Create Sample Review 
    def create_sample_review(self):
        """ Helper method to create a sample review """
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "user123",
            "place_id": "place123",
            "rating": 4,
            "comment": "Nice stay!",
            "upload_image": ["https://example.com/image.jpg"]
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        return data

    #Create Tests
    def test_create_review_success(self):
        """ Test successful review creation """
        review = self.create_sample_review()
        self.assertEqual(review.get("rating"), 4)
        self.assertEqual(review.get("comment"), "Nice stay!")

    def test_create_review_invalid_rating(self):
        """ Test invalid rating (must be between 1 and 5) """
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "user123",
            "place_id": "place123",
            "rating": 10,
            "comment": "Invalid rating"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertIn("rating", data["error"].lower())

    def test_create_review_missing_fields(self):
        """ Test creation missing required fields """
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 4,
            "comment": "Incomplete data"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    # Read Tests
    def test_get_review_by_id(self):
        """ Test retrieving a review by ID """
        review = self.create_sample_review()
        review_id = review.get("id")

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), review_id)
        self.assertEqual(data.get("user_id"), "user123")

    def test_get_review_invalid_id(self):
        """ Test retrieving a review with invalid ID """
        response = self.client.get('/api/v1/reviews/invalidID')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    #Update Tests
    def test_update_review_success(self):
        """ Test successful review update by owner """
        review = self.create_sample_review()
        review_id = review.get("id")

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 5,
            "comment": "Even better!",
            "current_user_id": "user123"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("rating"), 5)
        self.assertEqual(data.get("comment"), "Even better!")

    def test_update_review_invalid_id(self):
        """ Test updating a review with an invalid ID """
        response = self.client.put('/api/v1/reviews/invalidID', json={
            "rating": 3,
            "comment": "Invalid test",
            "current_user_id": "user123"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    def test_update_review_forbidden_user(self):
        """ Test updating a review by non-owner (should fail) """
        review = self.create_sample_review()
        review_id = review.get("id")

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 2,
            "comment": "Not allowed",
            "current_user_id": "another_user"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", data)

    # List Tests by user_id and place_id
    def test_list_reviews_by_place(self):
        """ Test listing reviews by place_id """
        self.create_sample_review()
        response = self.client.get('/api/v1/reviews/place/place123')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("place_id"), "place123")

    def test_list_reviews_by_place_not_found(self):
        """ Test listing reviews by invalid place_id """
        response = self.client.get('/api/v1/reviews/place/noPlace')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", data)

    def test_list_reviews_by_user(self):
        """ Test listing reviews by user_id """
        self.create_sample_review()
        response = self.client.get('/api/v1/reviews/user/user123')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("user_id"), "user123")

    def test_list_reviews_by_user_not_found(self):
        """ Test listing reviews by invalid user_id """
        response = self.client.get('/api/v1/reviews/user/noUser')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)