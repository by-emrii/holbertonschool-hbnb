from app.models.base_model import BaseModel
from datetime import datetime
import uuid
from io import BytesIO
from PIL import Image as PILImage

class Review(BaseModel):
    """Represents a review left by a user for a place."""
    ALLOWED_FORMATS = {"JPEG", "PNG"}

    def __init__(self, user_id, place_id, rating, comment=None, upload_image=None):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()

        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.upload_image = upload_image if upload_image is not None else []

    #RATING
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is None or value == "":
            raise ValueError("Rating is required")
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = float(value)

    #COMMENT
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if value is None:
            self._comment = None
            return
        if not isinstance(value, str):
            raise TypeError("Comment must be a string")
        
        value = value.strip()
        if len(value) > 300:
            raise ValueError("Comment cannot exceed 300 characters")
        self._comment = value
    
    #UPLOAD IMAGE 
    @property
    def upload_image(self):
        return self._upload_image

    @upload_image.setter
    def upload_image(self, images):
        if not images:
            self._upload_image = []
            return
        
        if not isinstance(images, list):
            raise TypeError("upload_image must be a list of image URLs or files")
        
        validated_images = []
        for img in images:  # Allows URLs
            if isinstance(img, str):
                validated_images.append(img)
                continue
            
            # Allows filename, bytes
            if isinstance(img, tuple) and len(img) == 2:
                filename, img_bytes = img
                try:
                    with PILImage.open(BytesIO(img_bytes)) as pil_img:
                        if pil_img.format not in self.ALLOWED_FORMATS:
                            raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
                except Exception:
                    raise ValueError("Invalid image data or unsupported format")
                validated_images.append((filename, img_bytes))
                continue

            raise TypeError("Each image must be a string URL or a tuple (filename, bytes)")

        self._upload_image = validated_images

    #Update helper
    def update_from_dict(self, data: dict):
        """Update review fields with partial data."""
        if "rating" in data:
            self.rating = data["rating"]
        if "comment" in data:
            self.comment = data["comment"]
        if "upload_image" in data:
            self.upload_image = data["upload_image"]
        self.updated_at = datetime.now()

    #Serialisation for API
    def save(self):
        """Return a JSON-serializable representation of the review."""
        # generate virtual URLs only for stored images (tuples)
        image_urls = []
        for i, img in enumerate(self.upload_image):
            if isinstance(img, str):
                image_urls.append(img)  # keep original URL
            else:
                image_urls.append(f"/reviews/{self.id}/images/{i}")
        
        return {
            "id": getattr(self, "id", None),
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": image_urls,
            "created_at": getattr(self, "created_at", None).isoformat() if getattr(self, "created_at", None) else None,
            "updated_at": getattr(self, "updated_at", None).isoformat() if getattr(self, "updated_at", None) else None,
        }
