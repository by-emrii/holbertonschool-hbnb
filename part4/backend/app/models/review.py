from sqlalchemy import Table, Column, Integer, ForeignKey
from app import db
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Represents a review left by a user for a place."""
    __tablename__ = 'reviews'
    #User can only make one review per place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )

    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

    # foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    #RATING
    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    #TEXT
    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Text is required and cannot be empty")
        return value.strip()

    #Update helper
    def update_from_dict(self, data: dict):
        """Safely update fields from a dictionary input."""
        for field in ("rating", "text"):
        #for field in ("rating", "text", "upload_image"):
            if field in data:
                setattr(self, field, data[field])

    #Serialisation for API
    def to_dict(self): 
        """Return a JSON-serializable representation of the review.""" 
        from app.services.facade import facade
        
        # Fetch user and place
        user = facade.get_user(self.user_id)
        place = facade.get_place(self.place_id)

        # Return dictionary
        return {
            "id": self.id,
            "rating": self.rating,
            "text": self.text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": {
                "id": user.id,
                "name": " ".join(filter(None, [user.first_name, user.last_name]))
            },
            "place": None if place is None else {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "address": place.address,
                "price": place.price,
            }
        }