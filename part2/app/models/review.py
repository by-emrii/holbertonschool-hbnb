from app.models.base_model import BaseModel
from datetime import datetime
import uuid
from io import BytesIO
from PIL import Image as PILImage

class Review(BaseModel):
    """Represents a review left by a user for a place."""
    ALLOWED_FORMATS = {"JPEG", "PNG"}

    def __init__(self, user, place, rating, text, upload_image=None):
        super().__init__()
        self.user = user
        self.place = place
        self.rating = rating
        self.text = text
        self.upload_image = upload_image or []

    #USER
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("user must be a User instance")
        self._user = value

    #PLACE
    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError("place must be a Place instance")
        self._place = value

    #RATING
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    #TEXT
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Text is required and cannot be empty")
        self._text = value.strip()
    
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
        for img in images:
            if isinstance(img, str):
                validated_images.append(img)
            elif isinstance(img, tuple) and len(img) == 2:
                filename, img_bytes = img
                try:
                    with PILImage.open(BytesIO(img_bytes)) as pil_img:
                        if pil_img.format not in self.ALLOWED_FORMATS:
                            raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
                except Exception:
                    raise ValueError("Invalid image data or unsupported format")
                validated_images.append((filename, img_bytes))
            else:
                raise TypeError("Each image must be a string URL or a tuple (filename, bytes)")
        self._upload_image = validated_images

    #Update helper
    def update_from_dict(self, data: dict):
        if "rating" in data:
            self.rating = data["rating"]
        if "text" in data:
            self.text = data["text"]
        if "upload_image" in data:
            self.upload_image = data["upload_image"]
        self.updated_at = datetime.now()

    #Serialisation for API
    def to_dict(self):
        """Return a JSON-serializable representation of the review."""
        # generate virtual URLs only for stored images (tuples)
        image_urls = [
            img if isinstance(img, str) else f"/reviews/{self.id}/images/{i}"
            for i, img in enumerate(self.upload_image)
        ]
        return {
            "id": self.id,
            "user_id": self.user.id,
            "place_id": self.place.id,
            "rating": self.rating,
            "text": self.text,
            "upload_image": image_urls,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }