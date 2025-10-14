from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserService


class HBnBFacade:
    def __init__(self):
        # self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        self.user_service = UserService()

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

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
