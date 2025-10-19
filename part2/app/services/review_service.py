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
                raise ValueError(f"Missing required field: '{key}'")
        
        comment = review_data.get("comment")
        rating = review_data.get("rating")

        #user must provide a rating if the comment
        if comment and rating is None:
            raise ValueError("Rating is required")
        
        ## Create review object
        review = Review(
            user_id=review_data.get("user_id"),
            place_id=review_data.get("place_id"),
            rating=rating,
            comment=comment,
            upload_image=review_data.get("upload_image")
        )
        self.review_repo.add(review)
        return review.save()
    
    def get_reviews_by_user(self, user_id):
        """Fetch all reviews made by a specific user."""
        if user_id is None:
            return []
        if not isinstance(user_id, (int, str)):
            raise TypeError("Unable to fetch review")
        
        filtered = [r.save() for r in self.review_repo.get_all() if r.user_id == user_id]
        return filtered
        
    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        if place_id is None:
            return []
        if not isinstance(place_id, (int, str)):
            raise TypeError("Place id must be int or str")
        
        filtered = [r.save() for r in self.review_repo.get_all() if r.place_id == place_id]
        return filtered
    
    def update_review(self, review_id, review_data, current_user_id):
        """User updates a review of a specific place"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        #Only the author can update
        if review.user_id != current_user_id:
            raise PermissionError("You are not allowed to update this review")\

        #Update allowed fields
        for field in ["rating", "comment", "upload_image"]:
            if field in review_data:
                setattr(review, field, review_data[field])
        #InMemoryRepository.update
        self.review_repo.update(review.id, {
            field: getattr(review, field) for field in ["rating", "comment", "upload_image"]
        })

        return review.save()

    def get_average_rating(self, place_id):
        """Calculate satistics rating"""
        if place_id is None:
            return 0
        if not isinstance(place_id, (int, str)):
            raise TypeError("Place id must be int or str")

        reviews = self.get_reviews_for_place(place_id)
        ratings = [r["rating"] for r in reviews if r.get("rating") is not None]

        return sum(ratings) / len(ratings) if ratings else 0
        
    def get_recent_reviews(self, place_id, limit=5):
        """Recent reviews displayed"""
        reviews = self.get_reviews_for_place(place_id)
        sorted_reviews = sorted(reviews, key=lambda r: r.get("created_at"), reverse=True)
        return sorted_reviews[:limit]
    
    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}

    def save(self):
        """Return a JSON-serializable dictionary of the review."""
        data = {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": self.upload_image or []  
        }
        return data
