from app.models.base_model import BaseModel
from datetime import datetime
import uuid
from io import BytesIO
from PIL import Image as image_upload

class Review(BaseModel):
    ALLOWED_FORMATS = {"JPEG", "PNG"}

    def __init__(self, user_id, place_id, rating, comment, upload_image=None):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.upload_image = upload_image

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
        self._rating = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if value is None or str(value).strip() == "":
            self._comment = None
            return
        if not isinstance(value, str):
            raise TypeError("Comment must be a string")
        value = value.strip()
        if len(value) > 100:
            raise ValueError("Comment cannot exceed 100 characters")
        self._comment = value

    @property
    def upload_image(self):
        return self._upload_image

    @upload_image.setter
    def upload_image(self, images):
        if images is None:
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
                    with image_upload.open(BytesIO(img_bytes)) as pil_img:
                        if pil_img.format not in self.ALLOWED_FORMATS:
                            raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
                except Exception:
                    raise ValueError("Each upload must be a valid image")
                validated_images.append(img)
            else:
                raise TypeError("Each image must be a URL string or a tuple (filename, bytes)")
        self._upload_image = validated_images

    def save(self):
        """Return dictionary representation for API responses"""
        image_urls = [f"/reviews/{self.id}/images/{i}" for i in range(len(self.upload_image))]
        return {
            "id": getattr(self, "id", None),
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": image_urls,
            "created_at": getattr(self, "created_at", None),
            "updated_at": getattr(self, "updated_at", None)
        }