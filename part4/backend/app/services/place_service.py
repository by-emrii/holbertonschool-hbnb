from app.models.place import Place
from app import db


class PlaceService():
    def __init__(self, place_repo, user_repo=None, amenity_repo=None, review_repo=None):
        self.user_repo = user_repo     # validate owner_id in user_repo 
        self.amenity_repo = amenity_repo  # validate amenity_id in amenity_repo
        self.place_repo = place_repo
        self.review_repo = review_repo  # validate review_id


    # ---------- Create Place ----------
    def create_place(self, place_data: dict):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid payload")

        if "profile_img" in place_data and "image_url" not in place_data:
             place_data["image_url"] = place_data.pop("profile_img")

        # Validate owner
        owner_id = place_data.get("owner_id")
        if self.user_repo and owner_id:
            if self.user_repo.get(owner_id) is None:
                raise ValueError("Owner (owner_id) not found")

        # pull out amenity ids first by using pop
        amenity_ids = place_data.pop("amenity_ids", None)

        # Create the place without amenity_ids
        place = Place(**place_data)
        self.place_repo.add(place)

        # Add amenities through the relationship
        if amenity_ids and self.amenity_repo:
            # Remove duplicates
            unique_amenity_ids = list(dict.fromkeys(str(v) for v in amenity_ids))
            for amenity_id in unique_amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    # call the helper method from model
                    place.add_amenity(amenity)
        # Repository add() already commits the session
        db.session.commit()
        return place

    # ---------- Read Place ----------
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("404: Place not found")
        return place

    # ---------- List All Places ----------
    def list_places(self):
        """
        Return a list[Place] of all places in the repository.
        """
        places = self.place_repo.get_all()
        if not places:
            raise ValueError("404: Places not found")
        return places


    # ---------- Update ----------
    def update_place(self, place_id, place_data:dict):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid payload")

        place = self.get_place(place_id)

        # Handle amenity_ids separately for relationship
        amenity_ids = place_data.pop("amenity_ids", None)

        # Update basic attr
        updatable = {
            "title",
            "description",
            "price",
            "address",
            "latitude",
            "longitude",
            "image_url",
            # "amenity_ids",            
        }

        update_data = {}

        for key, value in place_data.items():
            if key in updatable and value is not None:
                setattr(place, key, value)               # validate by setter
                update_data[key] = getattr(place, key)   # assign the valiadated value to repo

        # Update amenities through the relationship if provided
        if amenity_ids is not None and self.amenity_repo:
            # Remove duplicates
            unique_amenity_ids = list(dict.fromkeys(str(v) for v in amenity_ids))
            # Clear existing amenities and add new ones
            place.amenities.clear()
            for amenity_id in unique_amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        # update repo（update(obj_id, data)）
        self.place_repo.update(place.id, update_data)
        db.session.commit()
        return place

    # ---------- Relationship: Amenity ----------
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place through the SQLAlchemy relationship"""
        place = self.get_place(place_id)
        # Validate amenity exists
        if self.amenity_repo and amenity_id:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")

            # Check if amenity is already associated with this place
            if amenity not in place.amenities:
                place.add_amenity(amenity)
                db.session.commit()

        return place

    # ---------- Relationship Method: Review ----------
    def add_review_to_place(self, place_id, review_id):
    # Reviews are now created with place_id directly, establishing the relationship
    # through the foreign key. This method is kept for backward compatibility but may not be needed?
        """ 
        Attach an existing Review to a Place.
        Typically used when a review is created separately.
        """
        place = self.get_place(place_id)
        if not self.review_repo:
            raise ValueError("Review repository not configured")

        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")

        place.add_review(review)
        db.session.commit()
        return place

    # ---------- Delete Place ----------
    def delete_place(self, place_id):
        """
        Delete a place by ID.
        This will also handle the cascade deletion of related reviews
        and removal of associations with amenities.
        """
        place = self.get_place(place_id)
        if place:
            # SQLAlchemy will handle:
            # 1. Cascade delete of reviews (cascade is set in place model)
            # 2. Removal of place_amenities associations (this will be done by SQLAlchemy ORM)
            self.place_repo.delete(place_id)
        else:
            raise ValueError(f"Place with id {place_id} does not exist")
