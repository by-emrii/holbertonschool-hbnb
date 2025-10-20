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
        review = Review(**self.review_data)
        self.assertEqual(review.user_id, "user123")
        self.assertEqual(review.place_id, "place123")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good stay")
        self.assertEqual(review.upload_image, ["https://example.com/image.jpg"])

    # Rating Validation
    def test_rating_validation(self):
        """Rating must be between 1 and 5"""
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "rating": 0})
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "rating": 6})

    # Comment Validation
    def test_comment_validation(self):
        """Comment cannot exceed 300 characters"""
        long_comment = "a" * 301
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "comment": long_comment})

    # Upload Image Validation
    def test_upload_image_validation(self):
        """upload_image must be a list of URLs or valid file tuples"""
        # Invalid type in list
        with self.assertRaises(TypeError):
            Review(**{**self.review_data, "upload_image": [123]})
        # Invalid file content simulation
        fake_bytes = b"notanimage"
        with self.assertRaises(ValueError):
            Review(**{**self.review_data, "upload_image": [("fake.jpg", fake_bytes)]})

if __name__ == "__main__":
    unittest.main(verbosity=2)
