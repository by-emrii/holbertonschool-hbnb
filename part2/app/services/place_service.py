from app.models.place import Place
from app.persistence.repository import InMemoryRepository


class PlaceService():
    def __init__(self, place_repo, user_repo=None):
        self.user_repo = user_repo     # validate owner_id in user_repo 
        self.place_repo = place_repo


    # ---------- Create Place ----------
    def create_place(self, place_data: dict):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid payload")

        if "profile_img" in place_data and "image_url" not in place_data:
             place_data["image_url"] = place_data.pop("profile_img")

        # Validate user_id and owner
        owner_id = place_data.get("user_id")
        if self.user_repo and owner_id:
            if self.user_repo.get(owner_id) is None:
                raise ValueError("Owner (user_id) not found")

        # Remove duplicate amenity_ids
        if "amenity_ids" in place_data and place_data["amenity_ids"] is not None:
            place_data["amenity_ids"] = list(dict.fromkeys(place_data["amenity_ids"]))

        place  = Place(**place_data)
        self.place_repo.add(place)
        return place

    # ---------- Read Place ----------
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("404: Place not found")
        return place

    # ---------- Update ----------
    def update_place(self, place_id, place_data:dict):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid payload")

        place = self.get_place(place_id)

        # Remove duplicate amenity_ids(if there is)
        if "amenity_ids" in place_data and place_data["amenity_ids"] is not None:
            place_data["amenity_ids"] = list(dict.fromkeys(place_data["amenity_ids"]))

        # Update attr
        updatable = {
            "title",
            "description",
            "price",
            "address",
            "latitude",
            "longitude",
            "image_url",
            "amenity_ids",            
        }

        update_data = {}

        for key, value in place_data.items():
            if key in updatable and value is not None:
                setattr(place, key, value)               # validate by setter
                update_data[key] = getattr(place, key)   # assign the valiadated value to repo

        # update repo（update(obj_id, data)）
        self.place_repo.update(place.id, update_data)
        return place
