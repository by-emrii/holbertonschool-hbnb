from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class AmenityService:
    def __init__(self):
        """ Instantiate Amenity Repo where data is stored """
        self.amenity_repo = InMemoryRepository()
    
    """ Add an amenity """
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        # check if amenity exists
        check_amenity = self.amenity_repo.get(amenity.id)
        if check_amenity:
            # if amenity exists, return existing amenity id
            return self.amenity_repo.get(amenity.id), "Amenity already exists"
        else:
            # if amenity does not exist
            self.amenity_repo.add(amenity)
            return amenity
    
    """ Get an amenity """
    def get_amenity(self, amenity_id):
        check_amenity = self.amenity_repo.get(amenity_id)
        if check_amenity:
            return check_amenity
        else:
            raise ValueError(f"Amenity id {amenity_id} does not exist")
        
    """ Get all amenities """
    def get_all_amenities(self):
        if self.amenity_repo.get_all() is None:
            raise ValueError('No amenities found') 
        else:
            return self.amenity_repo.get_all()

    """ Update amenities """
    def update_amenity(self, amenity_id, amenity_data):
        # Validate input data
        name = amenity_data.get("name")
        if not name:
            raise ValueError('Invalid Input data - name is required')
        
        # get amenity
        existing_amenity = self.get_amenity(amenity_id)
        if existing_amenity:
            self.amenity_repo.update(amenity_id, amenity_data)
            return existing_amenity
        else:
            raise ValueError('Amenity not found')