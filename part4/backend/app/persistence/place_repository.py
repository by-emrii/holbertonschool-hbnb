from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Retrieve all places owned by a specific user."""
        return self.model.query.filter_by(owner_id=owner_id).all()

    def get_places_by_price_range(self, min_price, max_price):
        """Retrieve places within a specific price range."""
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()

    def get_places_by_location(self, min_lat, max_lat, min_lon, max_lon):
        """Retrieve places within a geographic bounding box."""
        return self.model.query.filter(
            self.model.latitude >= min_lat,
            self.model.latitude <= max_lat,
            self.model.longitude >= min_lon,
            self.model.longitude <= max_lon
        ).all()


    def get_average_rating_for_place(self, place_id):
        """Calculate the average rating for a place"""
        average_rating = (
            db.session.query(func.avg(self.model.rating))
            .filter(self.model.place_id == place_id)
            .scalar()
        )

        if average_rating is None:
            return None

        # round to one decimal
        return round(float(average_rating), 1)