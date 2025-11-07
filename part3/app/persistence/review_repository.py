from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository
from sqlalchemy import func



class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    #def get_reviews_by_id(self, review_id): REDUNDANT -- DELETE PLEASE
        #"""list all reviews"""

    def get_reviews_by_user(self, user_id):
        """List all reviews by users"""
        return self.model.query.fliter_by(user_id=user_id).all()
    
    def get_reviews_for_place(self, place_id):
        """List all reviews for a place"""
        return self.model.query.fliter_by(place_id=place_id).all()
    
    def user_alredy_reviewed(self, place_id, user_id):
        """user cannot comment more than once"""
        return self.model.query.filter_by(place_id=place_id, user_id=user_id).first() is not None


    def get_average_rating_for_place(self, place_id):
        """Calculate the average rating for a place"""
        average_rating = (
            db.session.query(func.avg(self.model.rating))
            .filter(self.model.place_id == place_id)
            .scalar()
        )
        return float(average_rating) if average_rating is not None else None
    