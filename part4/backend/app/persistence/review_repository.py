from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)


    def get_all(self):
        """Fetch all reviews from the database."""
        return Review.query.all()
    
    def get_reviews_for_place(self, place_id):
        """List all reviews for a place"""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def user_already_reviewed(self, place_id, user_id):
        """user cannot comment more than once"""
        return self.model.query.filter_by(place_id=place_id, user_id=user_id).first() is not None

