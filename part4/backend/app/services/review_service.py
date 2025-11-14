from app.models.review import Review
from app import db


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
            user_id=user.id,
            place_id=place.id,
            rating=review_data["rating"],
            text=review_data["text"],
            #upload_image=review_data.get("upload_image", [])
        )

        # Save to repository
        self.review_repo.add(review)
        return review
    
    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.get_all()
    
    def user_already_reviewed(self, place_id, user_id):
        """
        Check if a user has already reviewed a specific place.
        Returns True if a review exists, False otherwise.
        """
        return self.review_repo.user_already_reviewed(place_id, user_id)

    #READ
    def get_review_by_id(self, review_id):
        """Fetch a single review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review not found")
        return review

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place (by ID)."""
        return self.review_repo.get_reviews_for_place(place_id)
    
    #UPDATE
    def update_review(self, review_id, review_data, current_user, is_admin=False):
        """
        Update a review if the current user is the author.
        """
        review = self.get_review_by_id(review_id)
        # Ownership check
        if not is_admin and str(review.user_id) != str(current_user):
            raise PermissionError("Unauthorised action")

        self.review_repo.update(review_id, review_data)
        return review

    #DELETE
    def delete_review(self, review_id, current_user, is_admin=False):
        """Delete a review by ID."""
        review = self.get_review_by_id(review_id)

        # Ownership check
        if not is_admin and str(review.user_id) != str(current_user):
            raise PermissionError("Unauthorized action.")

        # Delete the review
        self.review_repo.delete(review_id)
        return True

    #GETTING THE AVERAGE RATING AND RECENT REVIEWS
    #def get_average_rating(self, place_id):
        #"""Calculate average rating for a place."""
        #avg = self.review_repo.get_average_rating_for_place(place_id)
        #return round(avg, 2) if avg else 0

    #def get_recent_reviews(self, place_id, limit=5):
        #"""Return the most recent reviews for a place."""
        #reviews = self.review_repo.get_reviews_for_place(place_id)
        #return sorted(reviews, key=lambda r: r.created_at, reverse=True)[:limit]
    
    
    