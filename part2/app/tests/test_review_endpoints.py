import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestReviewEndpoint(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()

        #Create test users
        self.user = self.facade.create_user({
            'first_name': 'Reviewer',
            'last_name': 'User',
            'email': 'reviewer@example.com'
        })
        self.owner = self.facade.create_user({
            'first_name': 'Owner',
            'last_name': 'User',
            'email': 'owner@example.com'
        })

        #Create a test place
        self.place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'A test place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'user_id': self.owner.id
        })

    #Helper
    def create_sample_review(self, rating=5, text="Great place!"):
        return self.facade.create_review({
            'user_id': self.user.id,
            'place_id': self.place.id,
            'rating': rating,
            'comment': text
        })

    #Tests
    def test_create_review(self):
        review = self.create_sample_review()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great place!")

    def test_get_review_by_id(self):
        review = self.create_sample_review()
        retrieved = self.facade.get_review_by_id(review.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, review.id)

    def test_get_reviews_by_user(self):
        self.create_sample_review(rating=4)
        self.create_sample_review(rating=5)
        reviews = self.facade.get_reviews_by_user(self.user.id)
        self.assertEqual(len(reviews), 2)

    def test_get_reviews_for_place(self):
        self.create_sample_review(rating=4)
        self.create_sample_review(rating=3)
        reviews = self.facade.get_reviews_for_place(self.place.id)
        self.assertEqual(len(reviews), 2)

    def test_update_review(self):
        review = self.create_sample_review(rating=3, text="It was okay")
        updated_review = self.facade.update_review({
            'review_id': review.id,
            'review_data': {'rating': 5, 'comment': "Actually amazing!"},
            'current_user_id': self.user.id
        })
        self.assertEqual(updated_review.rating, 5)
        self.assertEqual(updated_review.comment, "Actually amazing!")

    def test_update_review_unauthorized(self):
        review = self.create_sample_review()
        response = self.facade.update_review({
            'review_id': review.id,
            'review_data': {'rating': 1},
            'current_user_id': 'other_user'
        })
        self.assertIn('error', response)

    def test_delete_review(self):
        review = self.create_sample_review()
        self.facade.delete_review(review.id)
        retrieved = self.facade.get_review_by_id(review.id)
        self.assertIsNone(retrieved)

    def test_average_rating(self):
        self.create_sample_review(rating=5)
        self.create_sample_review(rating=3)
        avg = self.facade.get_average_rating(self.place.id)
        self.assertEqual(avg, 4.0)

    def test_recent_reviews_limit(self):
        for i in range(10):
            self.create_sample_review(rating=i+1)
        recent = self.facade.get_recent_reviews(self.place.id, limit=5)
        self.assertEqual(len(recent), 5)
        self.assertEqual(recent[0].rating, 10)  #Most recent should be the highest rating

if __name__ == "__main__":
    unittest.main(verbosity=2)