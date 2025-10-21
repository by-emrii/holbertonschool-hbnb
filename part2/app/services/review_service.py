from datetime import datetime
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class ReviewService:
    def __init__(self,place_repo, user_repo=None):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = InMemoryRepository()
    
    #CREATE
    def create_review(self, review_data):
        """Create a review"""   
        #validate the input
        if not isinstance(review_data, dict):
            raise TypeError("Review data must be provided as a dictionary")
        
        # Validate required fields
        for key in ["user_id", "place_id", "rating"]:
            if key not in review_data or review_data[key] is None:
                raise ValueError(f"Missing required field: '{key}'")
        
        review = Review(
            user_id=review_data["user_id"],
            place_id=review_data["place_id"],
            rating=review_data.get("rating"),
            comment=review_data.get("comment"),
            upload_image=review_data.get("upload_image", [])
        )
        self.review_repo.add(review)
        return review
    
    #READ
    def get_review_by_id(self, review_id):
        """Fetch a single review by ID."""
        return self.review_repo.get(review_id)

    def get_reviews_by_user(self, user_id):
        """Fetch all reviews made by a specific user."""
        return [r for r in self.review_repo.get_all() if r.user_id == user_id]

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]
    
    #UPDATE
    def update_review(self, review_id, review_data, current_user_id):
        """Update a review if the current user is the author."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        # Only the author can update
        if review.user_id != current_user_id:
            raise PermissionError("You are not allowed to update this review")

        # Update allowed fields
        review.update_from_dict(review_data)
        self.review_repo.update(review.id, {
            "rating": review.rating,
            "comment": review.comment,
            "upload_image": review.upload_image
        })
        return review

    #GETTING THE AVERAGE RATING AND RECENT REVIEWS
    def get_average_rating(self, place_id):
        """Calculate average rating for a place."""
        reviews = self.get_reviews_for_place(place_id)
        ratings = [r.rating for r in reviews if getattr(r, "rating", None) is not None]
        return round(sum(ratings)/len(ratings), 2) if ratings else 0

    def get_recent_reviews(self, place_id, limit=5):
        """Return the most recent reviews for a place."""
        reviews = self.get_reviews_for_place(place_id)
        return sorted(reviews, key=lambda r: r.created_at, reverse=True)[:limit]
    
    #DELETE
    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}

    