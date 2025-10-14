from app.models.user import User
from app.persistence.repository import InMemoryRepository

class UserService:
    def __init__(self):
        self.user_repo = InMemoryRepository()
    
    def create_user(self, user_data):
        existing = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing:
            raise ValueError('Email already used - choose another email')
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError('404: User not found')
        
        """Validation check if new email passed in already has user profile attached"""
        current_email =user_data.get("email")
        if current_email is not None:
            new_email = current_email.strip().lower()

        existing_user = self.repo.get_by_attribute("email", new_email)

        if existing_user is not None and existing_user.id != user.id:
            return None, f"Email already in use: {new_email}"

        if new_email != user.email:
            user.email = new_email

        for key, value in user_data.items():
            setattr(user, key, value)

        