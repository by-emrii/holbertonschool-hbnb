from app.persistence.repository import InMemoryRepository
from app.review.review_service import ReviewService


class ReviewFacade:
    def __init__(self):
        self.review_repo = InMemoryRepository()
        self.review_service =  ReviewService(self.review_repo)

    def create_review(self, review_data):
        """Create and save a review."""
        try:
            return self.review_service.create_review(review_data)
        except ValueError as error:
            #in the case of empty comments and invalid rating
            return {"error":str(error)}
        except Exception as error:
            return {"error": f"Unexpected error: {str(error)}"}

    def get_reviews_by_user(self, user_id):
        """Fetch all reviews made by a specific user."""
        return self.review_service.get_reviews_by_user(user_id)

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        return self.review_service.get_reviews_for_place(place_id)
    
    def update_review(self, review_update):
        """User updates a review of a specific place"""
        try:
            review_id = review_update.get("review_id")
            review_data = review_update.get("review_data")
            current_user_id = review_update.get("current_user_id")
            return self.review_service.update_review(review_id, review_data, current_user_id)
        except ValueError as error:
            return {"error": str(error)}
        except PermissionError as error:
            return {"error": str(error)}
        except Exception as error:
            return{"error": f"Unexpected error: {str(error)}"}
        
    def get_average_rating(self, place_id):
        """Calculate satistics rating"""
        return self.review_service.get_average_rating(place_id)
    
    def get_recent_reviews(self, place_id, limit=5):
        """Recent reviews displayed"""
        return self.review_service.get_recent_reviews(place_id, limit)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        try:
            return self.review_service.delete_review(review_id)
        except ValueError as error:
            return {"error": str(error)}
        except Exception as error:
            return {"error": f"Unexpected error: {str(error)}"}
    
