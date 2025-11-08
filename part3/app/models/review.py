from sqlalchemy import Table, Column, Integer, ForeignKey
from app import db
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
#from app.services.facade import facade
#from io import BytesIO
#from PIL import Image as PILImage

class Review(BaseModel):
    """Represents a review left by a user for a place."""
    __tablename__ = 'reviews'
    #ALLOWED_FORMATS = {"JPEG", "PNG"}

    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    #upload_image = db.Column(db.JSON, default=list)

    # foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    #RATING
    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    #TEXT
    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Text is required and cannot be empty")
        return value.strip()
    
    #UPLOAD IMAGE 
    #@validates('upload_image')
    #def validate_upload_image(self, key, images):
        #if not images:
            #self._upload_image = []
            #return

        #if not isinstance(images, list):
            #raise TypeError("upload_image must be a list of image URLs or files")

        #validated_images = []
        #for img in images:
                #if isinstance(img, str):
                    #validated_images.append(img)
                #elif isinstance(img, tuple) and len(img) == 2:
                #filename, img_bytes = img
                #try:
                    #with PILImage.open(BytesIO(img_bytes)) as pil_img:
                        #if pil_img.format not in self.ALLOWED_FORMATS:
                            #raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
                #except Exception:
                    #raise ValueError("Invalid image data or unsupported format")
                #validated_images.append((filename, img_bytes))
            #else:
                #raise TypeError("Each image must be a string URL or a tuple (filename, bytes)")
        #return validated_images

    #Update helper
    def update_from_dict(self, data: dict):
        """Safely update fields from a dictionary input."""
        for field in ("rating", "text"):
        #for field in ("rating", "text", "upload_image"):
            if field in data:
                setattr(self, field, data[field])

    #Serialisation for API
    def to_dict(self): 
        """Return a JSON-serializable representation of the review.""" 
        # generate virtual URLs only for stored images (tuples) 
        #image_urls = []
        #for i, img in enumerate(self.upload_image or []):
            #if isinstance(img, str):
                #image_urls.append(img)
            #elif isinstance(img, dict) and "filename" in img:
                #image_urls.append(f"/reviews/{self.id}/images/{i}")
            #else:
                #image_urls.append(None)
        from app.services.facade import facade
        
        # Safely fetch user
        user = facade.get_user(self.user_id)
        if user is None:
            user_info = {"id": None, "name": "Deleted user"}
        else:
            user_info = {
                "id": user.id,
                "name": " ".join(filter(None, [getattr(user, "first_name", None), getattr(user, "last_name", None)])),
            }
        
        # Fetch place safely
        place = facade.get_place(self.place_id)
        if place is None:
            place_info = None  # review will be filtered out elsewhere if place deleted
        else:
            place_info = {
                "id": place.id,
                "title": getattr(place, "title", None),
                "description": getattr(place, "description", None),
                "address": getattr(place, "address", None),
                "price": getattr(place, "price", None),
            }

        return {
            "id": self.id,
            "rating": self.rating,
            "text": self.text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": user_info,
            "place": place_info,
        }