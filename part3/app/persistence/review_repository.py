from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    #def get_reviews_by_id(self, review_id): THIS NEEDS TO BE DELETED
        #"""list all reviews"""

    def get_reviews_by_user(self, user_id):
        """list all reviews by users"""
        return self.model.query.fliter_by(user_id=user_id).all()
    
    def get_review_by_place(self, place_id):
        """List all reviews for a place"""
        return self.model.query.fliter_by(place_id=place_id).all()
    
    #def get_average_rating_for_place(self, place_id):
        #"""Calculate the average rating for a place"""
        #average_rating = db.session.query(func.avg(self.model.rating)).fliter(self.model.place_id == place_id).scalar()
        #return float(average_rating) if average_rating is not None else None
    