from app.persistence.repository import InMemoryRepository
from app.review.review_service import ReviewService


class ReviewFacade:
    def __init__(self):
        self.review_repo = InMemoryRepository()
        self.review_service =  ReviewService(self.review_repo)

    def create_review(self, data):
        """Create and save a review."""
        try:
            return self.review_service.create_review(data)
        except ValueError as error:
            #in the case of empty comments and invalid rating
            return {"error":str(error)}
        except Exception as error:
            return {"error": f"Unexpected error: {str(error)}"}

    def get_reviews_by_user(self, userId):
        """Fetch all reviews made by a specific user."""
        return self.review_service.get_reviews_by_user(userId)

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        return self.review_service.get_reviews_for_place(place_id)
        
    def delete_review(self, review_id):
        """Delete a review by ID."""
        return self.review_service.delete_review(review_id)
    
