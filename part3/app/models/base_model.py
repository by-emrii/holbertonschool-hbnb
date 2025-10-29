import uuid
from datetime import datetime


class BaseModel:
    """
    Base Model provides attibutes and methods for all entities
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # update method
    def update(self, data = None):
        """Update updated_at timestamp."""
        if data:
            for key, value in data.items():
              if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    # create method
    # def create(self):
    #     """This method is called when the object is first created"""

    # # delete method
    # """Implement later"""
