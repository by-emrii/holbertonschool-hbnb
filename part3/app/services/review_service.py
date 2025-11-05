import unittest
from datetime import datetime
from app.models.review import Review

class ReviewService():
    def __init__(self, place_repo, user_repo, review_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = review_repo
    
    #CREATE
    def create_review(self, review_data):
        """Create a review"""
        user = review_data.get("user")
        place = review_data.get("place")

        if not user or not place:
            raise ValueError("User and Place objects are required")
        
        # Create review instance
        review = Review(
            user=user,
            place=place,
            rating=review_data["rating"],
            text=review_data["text"],
            upload_image=review_data.get("upload_image", [])
        )

        # Save to repository
        self.review_repo.add(review)
        return review
    
    def user_already_reviewed(self, place_id, user_id):
        """
        Check if a user has already reviewed a specific place.
        Returns True if a review exists, False otherwise.
        """
        for review in self.review_repo.get_all():
            if str(review.place.id) == str(place_id) and str(review.user.id) == str(user_id):
                return True
        return False

    #READ
    def get_review_by_id(self, review_id):
        """Fetch a single review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review '{review_id}' not found")
        return review

    def get_reviews_by_user(self, user_id):
        """Fetch all reviews made by a specific user (by ID)."""
        return [r for r in self.review_repo.get_all() if r.user.id == user_id]

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place (by ID)."""
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]
    
    #UPDATE
    def update_review(self, review_id, review_data, current_user):
        """
        Update a review if the current user is the author.
        """
        review = self.get_review_by_id(review_id)

        # Ownership check
        user_id = getattr(review.user, "id", review.user)
        if str(user_id) != str(current_user):
            raise PermissionError("Unauthorised action")

        # Update the model using Review's own method
        review.update_from_dict(review_data)
        # Pass the updated object back to repo
        self.review_repo.update(review_id, review_data)
        return review

    #GETTING THE AVERAGE RATING AND RECENT REVIEWS
    def get_average_rating(self, place_id):
        """Calculate average rating for a place."""
        reviews = self.get_reviews_for_place(place_id)
        ratings = [r.rating for r in reviews if r.rating is not None]
        return round(sum(ratings)/len(ratings), 2) if ratings else 0

    def get_recent_reviews(self, place_id, limit=5):
        """Return the most recent reviews for a place."""
        reviews = self.get_reviews_for_place(place_id)
        return sorted(reviews, key=lambda r: r.created_at, reverse=True)[:limit]
    
    #DELETE
    def delete_review(self, review_id, current_user):
        """Delete a review by ID."""
        review = self.get_review_by_id(review_id)

        # Ownership check
        user_id = getattr(review.user, "id", review.user)
        if str(user_id) != str(current_user):
            raise PermissionError("Unauthorized action.")

        # Delete the review
        self.review_repo.delete(review_id)
        return True