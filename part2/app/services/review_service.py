from datetime import datetime
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class ReviewService:
    def __init__(self):
        self.review_repo = InMemoryRepository()
    
    
    def create_review(self, review_data):
        """Create a review"""   
        #validate the input
        if not isinstance(review_data, dict):
            raise TypeError("Review data must be provided as a dictionary")
        
        # Validate required fields
        for key in ["user_id", "place_id"]:
            if key not in review_data:
                raise ValueError(f"Missign required field: '{key}'")
        
        comment = review_data.get("comment")
        rating = review_data.get("rating")

        #user must provide a rating if the comment
        if comment and rating is None:
            raise ValueError("Rating is required")
        
        ## Create review object
        review = Review(
            user_id=review_data.get("user_id"),
            place_id=review_data.get("place_id"),
            rating=review_data.get("rating"),
            comment=review_data.get("comment"),
            upload_image=review_data.get("upload_image")
        )
        self.review_repo.add(review)
        return review
    
    def get_reviews_by_user(self, user_id):
        """Fetch all reviews made by a specific user."""
        if user_id is None:
            return []
        if not isinstance(user_id, (int, str)):
            raise TypeError("Unable to fetch review")
        
        user_review = self.review_repo.get_all()
        filtered = [review for review in user_review if review.user_id == user_id]

        return filtered
        
    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        if place_id is None:
            return []
        if not isinstance(place_id, (int, str)):
            raise TypeError("Unable to fetch reviews")
        
        all_reviews = self.review_repo.get_all()
        filtered = [review for review in all_reviews if review.place_id == place_id]

        return filtered
    
    def update_review(self, review_id, review_data, current_user_id):
        """User updates a review of a specific place"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("404: Review not found")

        #Only the author can update
        if review.user_id != current_user_id:
            raise PermissionError("You are not allowed to update this review")
        
        comment = review_data.get("comment", review.comment)
        rating = review_data.get("rating", review.rating)

        #Update allowed fields
        allowed_fields = ["rating", "comment", "upload_image"]
        for field in allowed_fields:
            if field in review_data:
                setattr(review, field, review_data[field])

        self.review_repo.update(review)
        return review

    def get_average_rating(self, place_id):
        """Calculate satistics rating"""
        if place_id is None:
            return 0
        if not isinstance(place_id, (int, str)):
            raise TypeError("place id must be an integer or string")
        
        all_reviews = self.get_reviews_for_place(place_id)
        filtered = [review for review in all_reviews if review.place_id == place_id]
        ratings = [review.rating for review in filtered]

        if not ratings:
            return 0

        average = sum(ratings) / len(ratings)
        return average
        
    def get_recent_reviews(self, place_id, limit=5):
        """Recent reviews displayed"""
        if place_id is None:
            return []
        if not isinstance(place_id, (int, str)):
            raise TypeError("Unable to fetch reviews.")

        reviews = self.get_reviews_for_place(place_id)
        sorted_reviews = sorted(reviews, key=lambda r: r.created_at, reverse=True)
        return sorted_reviews[:limit]
    
    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not Found")
        
        self.review_repo.delete(review)
        return True
