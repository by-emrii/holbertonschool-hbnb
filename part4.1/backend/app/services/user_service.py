from app.models.user import User
from app import db

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    # Create user
    def create_user(self, user_data):
        existing = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing:
            raise ValueError('Email already used - choose another email')
        user = User(**user_data)
        user.hash_password(user_data['password']) # hash pwd before saving
        self.user_repo.add(user)
        return user

    # Get User by ID
    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('404: User not found')
        return user

    # Get user by email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Update User
    def update_user(self, user_id, user_data):
        # Get the current user
        user = self.get_user(user_id)

        # When the user's update request contains email, then valid it
        if 'email' in user_data and user_data['email'] is not None:
            new_email = user_data['email'].strip()

            # if new_email = current email, skip it
            if new_email != user.email:
                # check if the new email is already used in repo
                found_user = self.user_repo.get_by_attribute('email', new_email)
                # if new email not None(means it's in use by others)
                if found_user is not None and found_user.id != user.id:
                    raise ValueError(f"Email already in use: {new_email}")
                user.email = new_email
        
        # Handle password update
        if 'password' in user_data and user_data['password']:
            user.hash_password(user_data['password'])

        # To update the rest of attributes: name, number, image
        updatable = {
            "first_name",
            "last_name",
            "phone_number",
            "profile_img",
            "is_admin",
        }

        for key in updatable:
            if key in user_data and user_data[key] is not None:
                setattr(user, key, user_data[key])

        db.session.commit()

        return user

    # Get all users
    def get_all_users(self):
        users = self.user_repo.get_all()
        return users
