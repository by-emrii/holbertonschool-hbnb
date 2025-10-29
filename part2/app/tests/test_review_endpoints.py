import unittest
from app import create_app
from app.models.review import Review

class TestReviewModel(unittest.TestCase):
    def setUp(self):
        """Initialize app and default review data"""
        self.app = create_app()
        self.client = self.app.test_client()

    # Create Sample Review 
    def create_sample_review(self):
        """ Create review """
        """ Test creation of review """
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "user123",
            "place_id": "place123",
            "rating": 4.5,
            "comment": "Nice stay!",
            "upload_image": ["https://example.com/image.jpg"]
        })
        
        review_data = response.get_json()
        # Check fields in JSON response
        self.assertEqual(review_data.get("user_id"), "user123")
        self.assertEqual(review_data.get("place_id"), "place123")
        self.assertEqual(review_data.get("rating"), 4.5)
        self.assertEqual(review_data.get("comment"), "Nice stay!")
        self.assertEqual(response.status_code, 201)
        return response

    #Create Tests
    def test_create_review(self):
            """ Test successful review creation """
            self.create_sample_review()

    def test_create_review_invalid_rating(self):
        """ Rating must be between 1 and 5 """
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "user123",
            "place_id": "place123",
            "rating": 10,
            "comment": "Invalid rating"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertIn("rating", data.get("error", "").lower())

    def test_create_review_missing_fields(self):
        """ Missing required fields should fail """
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 4,
            "comment": "Incomplete data"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    # Get Tests
    def test_get_review_by_id(self):
        """ Test get review by review ID """
        create_resp = self.create_sample_review()
        review_data = create_resp.get_json()
        review_id = review_data.get("id")

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("id"), review_id)
        self.assertEqual(data.get("user_id"), "user123")

    def test_get_review_invalid_id(self):
        """ Test get review by invalid ID """
        response = self.client.get('/api/v1/reviews/invalidID')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

    #Update Tests
    def test_update_review_success(self):
        """ Test successful review update """
        create_resp = self.create_sample_review()
        review_data = create_resp.get_json()
        review_id = review_data.get("id")

        update_resp = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 5,
            "comment": "Even better!",
            "current_user_id": "user123"
        })
        data = update_resp.get_json()
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(data.get("rating"), 5)
        self.assertEqual(data.get("comment"), "Even better!")

    def test_update_review_invalid_id(self):
        """ Test update review with invalid ID """
        update_resp = self.client.put('/api/v1/reviews/invalidID', json={
            "rating": 3,
            "comment": "Invalid test",
            "current_user_id": "user123"
        })
        data = update_resp.get_json()
        self.assertEqual(update_resp.status_code, 404)
        self.assertIn("error", data)

    def test_update_review_forbidden_user(self):
        """ Only owner can update their review """
        create_resp = self.create_sample_review()
        review_data = create_resp.get_json()
        review_id = review_data.get("id")

        update_resp = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 2,
            "comment": "Not allowed",
            "current_user_id": "another_user"
        })
        data = update_resp.get_json()
        self.assertEqual(update_resp.status_code, 403)
        self.assertIn("error", data)

    # List Tests by user_id and place_id
    def test_list_reviews_by_place(self):
        """ Test listing reviews by place ID """
        self.create_sample_review()
        response = self.client.get('/api/v1/reviews/place/place123')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("place_id"), "place123")

    def test_list_reviews_by_place_not_found(self):
        """ No reviews found for invalid place """
        response = self.client.get('/api/v1/reviews/place/noPlace')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", data)

    def test_list_reviews_by_user(self):
        """ Test listing reviews by user ID """
        self.create_sample_review()
        response = self.client.get('/api/v1/reviews/user/user123')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0].get("user_id"), "user123")

    def test_list_reviews_by_user_not_found(self):
        """ No reviews found for invalid user """
        response = self.client.get('/api/v1/reviews/user/noUser')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", data)

if __name__ == "__main__":
    unittest.main(verbosity=2)