from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserService
from app.services.amenity_service import AmenityService
from app.services.reservation_service import ReservationService
from app.services.place_service import PlaceService

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        # self.amenity_repo = InMemoryRepository()

        self.user_service = UserService()
        self.amenity_service = AmenityService()
        self.reservation_service = ReservationService()
        self.place_service = PlaceService()

    """ User CRU """
    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        return self.user_service.create_user(user_data)

    # get user
    def get_user(self, user_id):
        return self.user_service.get_user(user_id)

    # get user by email
    def get_user_by_email(self, email):
        return self.user_service.get_user_by_email(email)

    # update user
    def update_user(self, user_id, user_data):
        return self.user_service.update_user(user_id, user_data)

    """ Place CRU """
    # Create place
    def create_place(self, place_data):
        return self.place_service.create_place(place_data)

    # Get Place
    def get_place(self, place_id):
        return self.place_service.get_place(place_id)

    # Update Place
    def update_place(self, place_id, place_data):
        return self.place_service.update_place(place_id, place_data)

    """ Amenity CRU """
    # create amenity
    def create_amenity(self, amenity_data):
        return self.amenity_service.create_amenity(amenity_data)

    # get amenity
    def get_amenity(self, amenity_id):
        return self.amenity_service.get_amenity(amenity_id)
    
    # get all amenities
    def get_all_amenities(self):
        return self.amenity_service.get_all_amenities()
    
    # update amenity
    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_service.update_amenity(amenity_id, amenity_data)

    """ Reservation CRU """
    # create reservation
    def create_reservation(self, reservation_data):
        return self.reservation_service.create_reservation(reservation_data)

    # get one reservation by ID
    def get_reservation(self, reservation_id):
        return self.reservation_service.get_reservation(reservation_id)

    # get all reservations
    def get_all_reservations(self):
        return self.reservation_service.get_all_reservations()

    # update an existing reservation
    def update_reservation(self, reservation_id, reservation_data):
        return self.reservation_service.update_reservation(reservation_id, reservation_data)
