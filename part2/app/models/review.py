from app.models.base_model import BaseModel
from datetime import datetime
import uuid
from PIL import Image as image_upload

class Review(BaseModel):
    ALLOWED_FORMATS = {"JPEG", "PNG"}

    def __init__(self, user_id, place_id, rating, comment, upload_image=None):
        super().__init__()
        self.user_id = userId
        self.place_id = placeId
        self.rating = rating
        self.comment = comment
        self.upload_image = upload_image

    """Rating"""
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is None or value == "":
            raise ValueError("Rating is required")
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number (int or float)")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5 stars")
        self._rating = value

    """Comment"""
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
            raise ValueError("Comment must not exceed 100 characters.")
        self._comment = value

    """Upload Image"""
    @property
    def upload_image(self):
        return self._upload_image

    @upload_image.setter
    def upload_image(self, images):
        if images is None:
            self._upload_image = []
            return

        if not isinstance(images, list):
            raise TypeError("upload_image must be a list of image files.")
        if len(images) > 4:
            raise ValueError("You can upload up to 4 images only.")

        validated_images = []
        for img in images:
            try:
                with image_upload.open(img) as pil_img:
                    if pil_img.format not in self.ALLOWED_FORMATS:
                        raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
                validated_images.append(img)
            except Exception:
                raise ValueError("Each upload must be a valid image file (JPEG or PNG).")

        self._upload_image = validated_images

    def save(self):
        data = super().save() or {}
        data.update({
            "userId": self.user_id,
            "placeId": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": self.upload_image
        })
        return data
