import unittest
from app import create_app
from app.models.review import Review

class TestReviewModel(unittest.TestCase):
    def setUp(self):
        """Initialize app and default review data"""
        self.app = create_app()
        self.client = self.app.test_client()

        # Default review data
        self.review_data = {
            "user_id": "user123",
            "place_id": "place123",
            "rating": 4,
            "comment": "Good stay",
            "upload_image": ["https://example.com/image.jpg"]
        }

    # Review Creation
    def test_review_creation(self):
        """Test that a review can be created with valid data"""
        print("Testing review creation...")
        review = Review(**self.review_data)
        print(f"Created review: {review.__dict__}")
        self.assertEqual(review.user_id, "user123")
        self.assertEqual(review.place_id, "place123")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good stay")
        self.assertEqual(review.upload_image, ["https://example.com/image.jpg"])

    # Create reviews via facade or API
    def test_list_reviews_by_place(self):
        from app.services import facade
        r1 = facade.create_review({"user_id": "user1", "place_id": "place123", "rating": 5, "comment": "Great!"})
        r2 = facade.create_review({"user_id": "user2", "place_id": "place123", "rating": 4, "comment": "Good!"})

        resp = self.client.get(f"/api/v1/reviews/place/place123")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(d["place_id"] == "place123" for d in data))

    # Rating Validation
    def test_rating_validation(self):
        """Rating must be between 1 and 5"""
        print("Testing rating validation...")
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "rating": 0})
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "rating": 6})
        print("Comment validation passed")

    # Comment Validation
    def test_comment_validation(self):
        """Comment cannot exceed 300 characters"""
        long_comment = "a" * 301
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "comment": long_comment})

    # Upload Image Validation
    def test_upload_image_validation(self):
        """upload_image must be a list of URLs or valid file tuples"""
        print("Testing upload_image validation...")
        # Invalid type in list
        with self.assertRaises(TypeError):
            Review(**{**self.review_data, "upload_image": [123]})
        # Invalid file content simulation
        fake_bytes = b"notanimage"
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "upload_image": [("fake.jpg", fake_bytes)]})
        print("Upload image validation passed")

if __name__ == "__main__":
    import unittest
    unittest.main(buffer=False, verbosity=2)
