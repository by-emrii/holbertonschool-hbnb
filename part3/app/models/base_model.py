from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Base Model provides attibutes and methods for all entities
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
