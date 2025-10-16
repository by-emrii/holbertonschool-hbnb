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
            if not isinstance(img, tuple) or len(img) != 2:
                raise TypeError("Each image must be a tuple: (filename:str, bytes)")
            filename, img_bytes = img
            try:
                with image_upload.open(BytesIO(img_bytes)) as pil_img:
                    if pil_img.format not in self.ALLOWED_FORMATS:
                        raise ValueError(f"Image must be JPEG or PNG (got {pil_img.format})")
            except Exception:
                raise ValueError("Each upload must be a valid image file (JPEG or PNG).")
            validated_images.append(img)

        self._upload_image = validated_images

    def save(self):
        data = super().save() or {}
        # Return URLs instead of raw bytes
        image_urls = [
            f"/reviews/{self.id}/images/{i}" for i in range(len(self.upload_image))
        ]
        data.update({
            "userId": self.user_id,
            "placeId": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": image_urls  # <-- use URLs here
        })
        return data
