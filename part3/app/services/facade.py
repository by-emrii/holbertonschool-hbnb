from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserService
from app.services.amenity_service import AmenityService
from app.services.reservation_service import ReservationService
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService

class HBnBFacade:
    def __init__(self):
        # shared repo
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.reservation_repo = InMemoryRepository()

        # services using shared repos
        self.user_service = UserService(self.user_repo)
        self.amenity_service = AmenityService()
        self.reservation_service = ReservationService()
        self.place_service = PlaceService(self.place_repo, self.user_repo)
        self.review_service = ReviewService(self.place_repo, self.user_repo, self.review_repo)
        
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

    # gel all users
    def get_all_users(self):
        return self.user_service.get_all_users()

    # update user
    def update_user(self, user_id, user_data):
        return self.user_service.update_user(user_id, user_data)

    """ Place CRU """
    # Create place
    def create_place(self, place_data):
        return self.place_service.create_place(place_data)

    # Get all places
    def list_places(self):
        return self.place_service.list_places()

    # Get a Place
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

    """Review CRU"""
    #CREATE A REVIEW
    def create_review(self, review_data):
        """Create and save a review."""
        return self.review_service.create_review(review_data)

    #IF USER ALREADY HAS A REVIEW
    def user_already_reviewed(self, place_id, user_id):
        """Check if a user has already reviewed a given place."""
        return self.review_service.user_already_reviewed(place_id, user_id)

    #READ REVIEWS
    def get_review_by_id(self, review_id):
        """Retrieve a single review by ID."""
        return self.review_service.get_review_by_id(review_id)

    def get_reviews_by_user(self, user_id):
        """Fetch all reviews for a specific user."""
        return self.review_service.get_reviews_by_user(user_id)

    def get_reviews_for_place(self, place_id):
        """Fetch all reviews for a specific place."""
        return self.review_service.get_reviews_for_place(place_id)

    def update_review(self, review_id, review_data, current_user):
        """User updates a review of a specific place."""
        return self.review_service.update_review(review_id, review_data, current_user)

    def delete_review(self, review_id, current_user):
        """User deletes a review."""
        return self.review_service.delete_review(review_id, current_user)

    def get_average_rating(self, place_id):
        """Calculate the average rating for a place."""
        return self.review_service.get_average_rating(place_id)

    def get_recent_reviews(self, place_id, limit=5):
        """Fetch the most recent reviews for a place."""
        return self.review_service.get_recent_reviews(place_id, limit)

    # Place add_amenity entry point
    def add_amenity_to_place(self, place_id, amenity_id):
        return self.place_service.add_amenity(place_id, amenity_id)
    # Place add_review entry
    def add_review_to_place(self, place_id, review_id):
        return self.place_service.add_review(place_id, review_id)

facade = HBnBFacade()